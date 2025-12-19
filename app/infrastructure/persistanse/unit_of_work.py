from contextlib import asynccontextmanager
from typing import Self, AsyncGenerator
from LuminUserService.app.domain.repositories.unit_of_work import UnitOfWork
from LuminUserService.app.infrastructure.cache.multi_level_cache import MultiLevelCache
from LuminUserService.app.infrastructure.persistanse.identity_map import UserIdentityMap
from LuminUserService.app.infrastructure.persistanse.postgres_sql_user_repository import PostgresSQLUserRepository


class UserUnitOfWork(UnitOfWork):
    def __init__(self, connection_factory, cache: MultiLevelCache) -> None:
        self.connection_factory = connection_factory
        self.identity_map: UserIdentityMap = UserIdentityMap()
        self.cache = cache

    async def __aenter__(self) -> Self:
        self.users = PostgresSQLUserRepository(
            connection_factory=self.connection_factory,
            identity_map=self.identity_map,
            cache=self.cache
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self.identity_map.clear()

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        self.identity_map.clear()


@asynccontextmanager
async def get_unit_of_work(connection_factory, cache: MultiLevelCache) -> AsyncGenerator[UserUnitOfWork, None]:
    uow = UserUnitOfWork(connection_factory, cache)
    async with uow:
        yield uow
