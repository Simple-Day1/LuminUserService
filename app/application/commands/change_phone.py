from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import PhoneNumber
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class ChangePhoneCommand:
    user_id: UUID
    new_phone: PhoneNumber


class ChangePhoneHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service: UserService = user_service
        self.event_bus: EventBus = event_bus

    async def handle(self, command: ChangePhoneCommand) -> dict[str, Any]:
        try:
            user: User = await self.user_service.change_phone(
                user_id=command.user_id,
                new_phone=command.new_phone
            )
            await self.event_bus.process_events(user)
            return {
                "success": True,
                "user_id": command.user_id,
                "new_phone": command.new_phone
            }

        except Exception as e:
            return {
                "success": False,
                "exception": str(e)
            }
