from uuid import UUID
from LuminUserService.app.domain.events.user_events import UserCreatedEvent
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import (
    Username, Date, PhoneNumber, Email, LanguageCode, Bio,
    AvatarURL, PrivacySettings
)
from LuminUserService.app.domain.models.entities.profile_view import ProfileView
from LuminUserService.app.infrastructure.cache.multi_level_cache import MultiLevelCache
from LuminUserService.app.infrastructure.persistanse.unit_of_work import get_unit_of_work


class UserService:
    def __init__(self, connection_factory, cache: MultiLevelCache) -> None:
        self.connection_factory = connection_factory
        self.cache = cache

    async def create_user(
            self,
            user_id: UUID,
            username: Username,
            date: Date | None,
            phone: PhoneNumber,
            email: Email | None,
            language_code: LanguageCode,
            bio: Bio | None,
            avatar_url: AvatarURL,
            privacy_settings: PrivacySettings,
            profile_views: list[ProfileView]
    ) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            existing_user = await uow.users.get_by_id(user_id)
            if existing_user:
                raise ValueError(f"User {user_id} already exists")

            user = User(
                user_id=user_id,
                username=username,
                date=date,
                phone=phone,
                email=email,
                language_code=language_code,
                bio=bio,
                avatar_url=avatar_url,
                privacy_settings=privacy_settings,
                profile_views=profile_views
            )

            user.add_domain_event(UserCreatedEvent(
                user_id=user_id,
                username=username,
                date=date,
                phone=phone,
                email=email,
                language_code=language_code,
                bio=bio,
                avatar_url=avatar_url,
                privacy_settings=privacy_settings,
                profile_views=profile_views
            ))

            await uow.users.save(user)
            await uow.commit()

            print(f"User created: {user_id}")
            return user

    async def change_username(self, user_id: UUID, new_username: Username) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.change_username(new_username)
            await uow.users.save(user)
            await uow.commit()
            return user

    async def change_date(self, user_id: UUID, new_date: Date) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            print("User Service change date method start")
            user = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.change_date(new_date)
            print("User Service change date method used")
            await uow.users.save(user)
            await uow.commit()
            return user

    async def change_email(self, user_id: UUID, new_email: Email) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user: User = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.change_email(new_email)
            await uow.users.save(user)
            await uow.commit()
            return user

    async def change_phone(self, user_id: UUID, new_phone: PhoneNumber) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user: User = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.change_phone(new_phone)
            await uow.users.save(user)
            await uow.commit()
            return user

    async def change_language_code(self, user_id: UUID, new_language_code: LanguageCode) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user: User = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.change_language_code(new_language_code)
            await uow.users.save(user)
            await uow.commit()
            return user

    async def change_bio(self, user_id: UUID, new_bio: Bio) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user: User = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.change_bio(new_bio)
            await uow.users.save(user)
            await uow.commit()
            return user

    async def change_avatar_url(self, user_id: UUID, new_avatar_url: AvatarURL) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user: User = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.change_avatar_url(new_avatar_url)
            await uow.users.save(user)
            await uow.commit()
            return user

    async def change_privacy_settings(self, user_id: UUID, new_privacy_settings: PrivacySettings) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            print("Start User Service change privacy settings method")
            user: User = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.change_privacy_settings(new_privacy_settings)
            await uow.users.save(user)
            await uow.commit()
            return user

    async def record_profile_view(self, user_id: UUID, viewer_id: UUID, viewer_ip: str) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user: User = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.record_profile_view(view_id=user_id, viewer_id=viewer_id, viewer_ip=viewer_ip)
            await uow.users.save(user)
            await uow.commit()
            return user

    async def block(self, user_id: UUID) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user: User = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.block()
            await uow.users.save(user)
            await uow.commit()
            return user

    async def activate(self, user_id: UUID) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user: User = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.activate()
            await uow.users.save(user)
            await uow.commit()
            return user

    async def deactivate(self, user_id: UUID) -> User:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user: User = await uow.users.get_by_id(user_id)

            if not user:
                raise ValueError(f"User {user_id} not found")

            user.deactivate()
            await uow.users.save(user)
            await uow.commit()
            return user

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            user: User = await uow.users.get_by_id(user_id)
            if user:
                print(f"[UserService.get_user_by_id] User found: {user}")
                print(f"[UserService.get_user_by_id] User class: {user.__class__}")
                print(f"[UserService.get_user_by_id] Has id attr: {hasattr(user, 'id')}")
                print(f"[UserService.get_user_by_id] User.id value: {user.id if hasattr(user, 'id') else 'NO ID'}")
            else:
                print(f"[UserService.get_user_by_id] User not found: {user_id}")
                raise ValueError(f"User {user_id} not found")

            return user

    async def delete(self, user_id: UUID) -> None:
        async with get_unit_of_work(self.connection_factory, self.cache) as uow:
            await uow.users.delete(user_id)
            await uow.commit()
