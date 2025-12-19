from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import AvatarURL
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class ChangeAvatarURLCommand:
    user_id: UUID
    new_avatar_url: AvatarURL


class ChangeAvatarURLHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service: UserService = user_service
        self.event_bus: EventBus = event_bus

    async def handle(self, command: ChangeAvatarURLCommand) -> dict[str, Any]:
        try:
            user: User = await self.user_service.change_avatar_url(
                user_id=command.user_id,
                new_avatar_url=command.new_avatar_url
            )

            await self.event_bus.process_events(user)

            return {
                "success": True,
                "user_id": command.user_id,
                "new_avatar_url": command.new_avatar_url
            }

        except Exception as e:
            return {
                "success": False,
                "exception": str(e)
            }
