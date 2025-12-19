from typing import Optional
from LuminUserService.app.application.commands.activate import ActivateHandler
from LuminUserService.app.application.commands.block import BlockHandler
from LuminUserService.app.application.commands.change_avatar_url import ChangeAvatarURLHandler
from LuminUserService.app.application.commands.change_bio import ChangeBioHandler
from LuminUserService.app.application.commands.change_date import ChangeDateHandler
from LuminUserService.app.application.commands.change_email import ChangeEmailHandler
from LuminUserService.app.application.commands.change_language_code import ChangeLanguageCodeHandler
from LuminUserService.app.application.commands.change_phone import ChangePhoneHandler
from LuminUserService.app.application.commands.change_privacy_settings import ChangePrivacySettingsHandler
from LuminUserService.app.application.commands.change_username import ChangeUsernameHandler
from LuminUserService.app.application.commands.deactivate import DeactivateHandler
from LuminUserService.app.application.commands.delete import DeleteHandler
from LuminUserService.app.application.commands.record_profile_view import RecordProfileViewHandler
from LuminUserService.app.infrastructure.persistanse.identity_map import UserIdentityMap
from LuminUserService.app.infrastructure.cache.multi_level_cache import MultiLevelCache
from LuminUserService.app.infrastructure.cache.redis_cache import CacheConfig, RedisCache
from LuminUserService.app.infrastructure.messaging.nats_event_bus import NatsEventBus
from LuminUserService.app.application.services.user_service import UserService
from LuminUserService.app.application.commands.create import CreateUserHandler
from LuminUserService.app.application.queries.get_by_id import GetUserByIdHandler


class DependencyContainer:
    def __init__(self, connection_factory, redis_config: Optional[CacheConfig] = None):
        self.connection_factory = connection_factory
        self.redis_config = redis_config or CacheConfig()
        self._event_bus = None
        self._user_service = None
        self._redis_cache = None
        self._multi_level_cache = None
        self._handlers = {}
        self._identity_map = None

    async def get_redis_cache(self) -> RedisCache:
        if not self._redis_cache:
            self._redis_cache = RedisCache(self.redis_config)
            await self._redis_cache.connect()
        return self._redis_cache

    def get_identity_map(self) -> UserIdentityMap:
        if not self._identity_map:
            from LuminUserService.app.infrastructure.persistanse.identity_map import UserIdentityMap
            self._identity_map = UserIdentityMap()
        return self._identity_map

    async def get_multi_level_cache(self) -> MultiLevelCache:
        if not self._multi_level_cache:
            redis_cache = await self.get_redis_cache()
            identity_map = self.get_identity_map()
            self._multi_level_cache = MultiLevelCache(redis_cache, identity_map)
        return self._multi_level_cache

    async def get_event_bus(self) -> NatsEventBus:
        if not self._event_bus:
            self._event_bus = NatsEventBus()
            await self._event_bus.connect()
        return self._event_bus

    async def get_user_service(self) -> UserService:
        if not self._user_service:
            cache = await self.get_multi_level_cache()
            self._user_service = UserService(self.connection_factory, cache)
            print(f"UserService created with connection_factory: {self.connection_factory}")
        return self._user_service

    async def get_user_by_id_handler(self) -> GetUserByIdHandler:
        key = "get_user_by_id"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = GetUserByIdHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_create_user_handler(self) -> CreateUserHandler:
        key = "create_user"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = CreateUserHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_delete_user_handler(self) -> DeleteHandler:
        key = "delete_user"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = DeleteHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_change_username_handler(self) -> ChangeUsernameHandler:
        key = "change_username"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = ChangeUsernameHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_change_email_handler(self) -> ChangeEmailHandler:
        key = "change_email"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = ChangeEmailHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_change_phone_handler(self) -> ChangePhoneHandler:
        key = "change_phone"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = ChangePhoneHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_change_bio_handler(self) -> ChangeBioHandler:
        key = "change_bio"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = ChangeBioHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_change_date_handler(self) -> ChangeDateHandler:
        key = "change_date"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = ChangeDateHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_change_language_code_handler(self) -> ChangeLanguageCodeHandler:
        key = "change_language_code"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = ChangeLanguageCodeHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_change_avatar_url_handler(self) -> ChangeAvatarURLHandler:
        key = "change_avatar_url"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = ChangeAvatarURLHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_change_privacy_settings_handler(self) -> ChangePrivacySettingsHandler:
        key = "change_privacy_settings"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = ChangePrivacySettingsHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_activate_handler(self) -> ActivateHandler:
        key = "activate"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = ActivateHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_deactivate_handler(self) -> DeactivateHandler:
        key = "deactivate"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = DeactivateHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_block_handler(self) -> BlockHandler:
        key = "block"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = BlockHandler(user_service, event_bus)
        return self._handlers[key]

    async def get_record_profile_view_handler(self) -> RecordProfileViewHandler:
        key = "record_profile_view"
        if key not in self._handlers:
            event_bus = await self.get_event_bus()
            user_service = await self.get_user_service()
            self._handlers[key] = RecordProfileViewHandler(user_service, event_bus)
        return self._handlers[key]
