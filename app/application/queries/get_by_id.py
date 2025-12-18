from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class GetUserByIdQuery:
    user_id: UUID


class GetUserByIdHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service: UserService = user_service
        self.event_bus: EventBus = event_bus

    async def handle(self, command: GetUserByIdQuery) -> dict[str, Any]:
        try:
            user: User = await self.user_service.get_user_by_id(command.user_id)
            print(f"[GetUserByIdHandler] User object created: {user}")
            print(f"[GetUserByIdHandler] User type: {type(user)}")
            print(f"[GetUserByIdHandler] User id attr: {getattr(user, 'id', 'NO ID')}")
            print(f"[GetUserByIdHandler] User username attr: {getattr(user, 'username', 'NO USERNAME')}")
            print(f"[GetUserByIdHandler] User dir: {[attr for attr in dir(user) if not attr.startswith('_')]}")

            return {
                "success": True,
                "user_id": command.user_id,
                "user": user
            }

        except Exception as e:
            return {
                "success": False,
                "exception": str(e)
            }
