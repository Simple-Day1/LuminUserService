from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import Date
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class ChangeDateCommand:
    user_id: UUID
    new_date: Date


class ChangeDateHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service: UserService = user_service
        self.event_bus: EventBus = event_bus

    async def handle(self, command: ChangeDateCommand) -> dict[str, Any]:
        try:
            print(f"[ChangeDateHandler] Command received: user_id={command.user_id}, new_date={command.new_date}")
            print(f"[ChangeDateHandler] new_date type: {type(command.new_date)}")
            print(f"[ChangeDateHandler] new_date.value: {command.new_date.value}")

            user: User = await self.user_service.change_date(
                user_id=command.user_id,
                new_date=command.new_date
            )
            print(user.date)
            await self.event_bus.process_events(user)
            return {
                "success": True,
                "user_id": command.user_id,
                "new_date": command.new_date
            }

        except Exception as e:
            return {
                "success": False,
                "exception": str(e)
            }
