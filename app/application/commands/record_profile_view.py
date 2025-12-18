from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class RecordProfileViewCommand:
    user_id: UUID
    viewer_id: UUID
    viewer_ip: str


class RecordProfileViewHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service: UserService = user_service
        self.event_bus: EventBus = event_bus

    async def handle(self, command: RecordProfileViewCommand) -> dict[str, Any]:
        try:
            user: User = await self.user_service.record_profile_view(
                user_id=command.user_id,
                viewer_id=command.viewer_id,
                viewer_ip=command.viewer_ip
            )
            await self.event_bus.process_events(user)
            return {
                "success": True,
                "user_id": command.user_id,
            }
        except Exception as e:
            return {
                "success": False,
                "exception": str(e)
            }
