from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import LanguageCode
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class ChangeLanguageCodeCommand:
    user_id: UUID
    new_language_code: LanguageCode


class ChangeLanguageCodeHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service: UserService = user_service
        self.event_bus: EventBus = event_bus

    async def handle(self, command: ChangeLanguageCodeCommand) -> dict[str, Any]:
        try:
            user: User = await self.user_service.change_language_code(
                user_id=command.user_id,
                new_language_code=command.new_language_code
            )
            await self.event_bus.process_events(user)
            return {
                "success": True,
                "user_id": command.user_id,
                "new_language_code": command.new_language_code
            }

        except Exception as e:
            return {
                "success": False,
                "exception": str(e)
            }
