from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class DeleteCommand:
    user_id: UUID


class DeleteHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service: UserService = user_service
        self.event_bus: EventBus = event_bus

    async def handle(self, command: DeleteCommand) -> dict[str, Any]:
        try:
            await self.user_service.delete(command.user_id)
            return {
                "success": True,
                "user_id": command.user_id,
            }

        except Exception as e:
            return {
                "success": False,
                "exception": str(e)
            }
