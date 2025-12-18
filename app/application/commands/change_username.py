from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import Username
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class ChangeUsernameCommand:
    user_id: UUID
    new_username: Username


class ChangeUsernameHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service: UserService = user_service
        self.event_bus: EventBus = event_bus

    async def handle(self, command: ChangeUsernameCommand) -> dict[str, Any]:
        try:
            user: User = await self.user_service.change_username(
                user_id=command.user_id,
                new_username=command.new_username
            )
            await self.event_bus.process_events(user)
            return {
                "success": True,
                "user_id": command.user_id,
                "new_username": command.new_username
            }

        except Exception as e:
            return {
                "success": False,
                "exception": str(e)
            }
