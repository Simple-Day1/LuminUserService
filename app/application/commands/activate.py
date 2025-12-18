from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class ActivateCommand:
    user_id: UUID


class ActivateHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service = user_service
        self.event_bus = event_bus

    async def handle(self, command: ActivateCommand) -> dict[str, Any]:
        try:
            user = await self.user_service.activate(command.user_id)

            await self.event_bus.process_events(user)

            return {
                "success": True,
                "user_id": str(command.user_id),
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
