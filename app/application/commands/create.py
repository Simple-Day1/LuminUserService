from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import (Username, Date, PhoneNumber, Email, LanguageCode, Bio,
                                                                     AvatarURL, PrivacySettings)
from LuminUserService.app.domain.models.entities.profile_view import ProfileView
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class CreateUserCommand:
    user_id: UUID
    username: Username
    date: Date | None
    phone: PhoneNumber
    email: Email | None
    language_code: LanguageCode
    bio: Bio | None
    avatar_url: AvatarURL
    privacy_settings: PrivacySettings
    profile_views: list[ProfileView]


class CreateUserHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service: UserService = user_service
        self.event_bus: EventBus = event_bus

    async def handle(self, command: CreateUserCommand) -> dict[str, Any]:
        try:
            user: User = await self.user_service.create_user(
                user_id=command.user_id,
                username=command.username,
                date=command.date,
                phone=command.phone,
                email=command.email,
                language_code=command.language_code,
                bio=command.bio,
                avatar_url=command.avatar_url,
                privacy_settings=command.privacy_settings,
                profile_views=command.profile_views,
            )
            await self.event_bus.process_events(user)
            return {
                "success": True,
                "user_id": command.user_id
            }

        except Exception as e:
            return {
                "success": False,
                "exception": str(e)
            }
