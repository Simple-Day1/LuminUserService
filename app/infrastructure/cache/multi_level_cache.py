from typing import Optional, Any
from uuid import UUID
from datetime import timedelta
import logging
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.infrastructure.cache.redis_cache import RedisCache
from LuminUserService.app.infrastructure.persistanse.identity_map import UserIdentityMap
from LuminUserService.app.infrastructure.persistanse.user_mapper import UserMapper

logger = logging.getLogger(__name__)


class MultiLevelCache:
    def __init__(self, redis_cache: RedisCache, identity_map: UserIdentityMap):
        self.redis = redis_cache
        self.identity_map = identity_map
        self.local_cache_ttl = timedelta(minutes=5)

    async def get_user(self, user_id: UUID) -> Optional[User]:
        cached_user = self.identity_map.get(user_id)
        if cached_user:
            logger.debug(f"User {user_id} found in Identity Map")
            return cached_user

        redis_user_data = await self.redis.get_user(user_id)
        if redis_user_data:
            redis_user = UserMapper().to_domain(data=redis_user_data)
        else:
            redis_user = None

        if redis_user:
            logger.debug(f"User {user_id} found in Redis")
            if hasattr(redis_user, '__dict__'):
                self.identity_map.add(redis_user)
            return redis_user

        logger.debug(f"User {user_id} not found in cache")
        return None

    async def set_user(self, user_id: UUID, user_data: dict) -> bool:
        try:
            self.identity_map.add(UserMapper().to_domain(user_data))

            ttl = 3600
            success = await self.redis.set_user(user_id, user_data, ttl)

            if success:
                logger.debug(f"User {user_id} cached in Redis")
            else:
                logger.warning(f"Failed to cache user {user_id} in Redis")

            return success
        except Exception as e:
            logger.error(f"Error caching user {user_id}: {e}")
            return False

    async def invalidate_user(self, user_id: UUID) -> bool:
        try:
            self.identity_map.remove(user_id)

            success = await self.redis.delete_user(user_id)

            await self.redis.invalidate_user_cache(user_id)

            logger.debug(f"Cache invalidated for user {user_id}")
            return success
        except Exception as e:
            logger.error(f"Error invalidating cache for user {user_id}: {e}")
            return False

    async def get_with_fallback(
            self,
            user_id: UUID,
            fallback_func,
            *args, **kwargs
    ) -> Optional[Any]:
        cached_data = await self.get_user(user_id)
        if cached_data:
            return cached_data

        fresh_data = await fallback_func(*args, **kwargs)

        if fresh_data:
            await self.set_user(user_id, fresh_data)

        return fresh_data
