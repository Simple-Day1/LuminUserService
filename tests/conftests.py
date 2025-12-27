import asyncio
import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import PrivacySettings, Username, Date, PhoneNumber, Email, \
    LanguageCode, Bio, AvatarURL
from LuminUserService.app.infrastructure.cache.multi_level_cache import MultiLevelCache
from LuminUserService.app.infrastructure.cache.redis_cache import CacheConfig, RedisCache
from LuminUserService.app.infrastructure.dependency_container import DependencyContainer
from LuminUserService.app.infrastructure.persistanse.identity_map import UserIdentityMap


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15-alpine") as container:
        container.start()
        yield container


@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:7-alpine") as container:
        container.start()
        yield container


@pytest.fixture(scope="session")
async def async_engine(postgres_container):
    engine = create_async_engine(
        postgres_container.get_connection_url().replace("psycopg2", "asyncpg"),
        echo=False,
        pool_pre_ping=True
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_session(async_engine):
    async with async_engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: sync_conn.execute("DROP SCHEMA public CASCADE"))
        await conn.run_sync(lambda sync_conn: sync_conn.execute("CREATE SCHEMA public"))

    async_session_factory = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def redis_cache(redis_container):
    config = CacheConfig(
        host=redis_container.get_container_host_ip(),
        port=redis_container.get_exposed_port(6379),
        default_ttl=60
    )
    cache = RedisCache(config)
    await cache.connect()
    yield cache
    await cache.disconnect()


@pytest.fixture
def identity_map():
    return UserIdentityMap()


@pytest.fixture
def mock_event_bus():
    mock = AsyncMock()
    mock.publish = AsyncMock()
    mock.subscribe = AsyncMock()
    mock.process_events = AsyncMock()
    return mock


@pytest.fixture
def privacy_settings():
    return PrivacySettings(
        profile_avatar_visibility_for_contacts=True,
        profile_avatar_visibility_for_all_users=True,
        profile_avatar_visibility_black_list=[],
        profile_avatar_visibility_white_list=[],
        profile_date_of_born_visibility_for_contacts=True,
        profile_date_of_born_visibility_for_all_users=True,
        profile_date_of_born_visibility_black_list=[],
        profile_date_of_born_visibility_white_list=[],
        profile_phone_number_visibility_for_contacts=True,
        profile_phone_number_visibility_for_all_users=True,
        profile_phone_number_visibility_black_list=[],
        profile_phone_number_visibility_white_list=[],
        profile_email_address_visibility_for_contacts=True,
        profile_email_address_visibility_for_all_users=True,
        profile_email_address_visibility_black_list=[],
        profile_email_address_visibility_white_list=[]
    )


@pytest.fixture
def sample_user_data():
    return {
        "user_id": uuid4(),
        "username": Username(first_name="John", last_name="Doe"),
        "date": Date(value=datetime.datetime.now()),
        "phone": PhoneNumber(value="+1234567890"),
        "email": Email(value="john.doe@example.com"),
        "language_code": LanguageCode(value="en"),
        "bio": Bio(value="Software Developer"),
        "avatar_url": AvatarURL(value="https://example.com/avatar.jpg"),
        "privacy_settings": PrivacySettings(),
        "profile_views": [],
        "status": "active"
    }


@pytest.fixture
def sample_user(sample_user_data):
    return User(**sample_user_data)


@pytest.fixture
def multilevel_cache(redis_cache, identity_map):
    return MultiLevelCache(redis_cache, identity_map)


@pytest.fixture
def mock_unit_of_work(mocker):
    mock_uow = mocker.AsyncMock()
    mock_uow.users = mocker.AsyncMock()
    mock_uow.commit = mocker.AsyncMock()
    mock_uow.rollback = mocker.AsyncMock()
    return mock_uow


@pytest.fixture
def mock_user_service(mocker, mock_unit_of_work):
    mock_service = mocker.AsyncMock()
    mock_service.uow_factory = mocker.AsyncMock(return_value=mock_unit_of_work)
    return mock_service


@pytest.fixture
def dependency_container(mocker, redis_cache):
    mock_connection_factory = mocker.Mock()
    container = DependencyContainer(mock_connection_factory)
    mocker.patch.object(container, "_redis_cache", redis_cache)
    return container




