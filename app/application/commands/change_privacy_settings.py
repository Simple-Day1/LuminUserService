from dataclasses import dataclass
from typing import Any
from uuid import UUID
from LuminUserService.app.domain.events.event_bus import EventBus
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import PrivacySettings
from LuminUserService.app.application.services.user_service import UserService


@dataclass
class ChangePrivacySettingsCommand:
    user_id: UUID
    new_privacy_settings: PrivacySettings


class ChangePrivacySettingsHandler:
    def __init__(self, user_service: UserService, event_bus: EventBus) -> None:
        self.user_service: UserService = user_service
        self.event_bus: EventBus = event_bus

    async def handle(self, command: ChangePrivacySettingsCommand) -> dict[str, Any]:
        try:
            print("Start handle changing of privacy settings")
            user: User = await self.user_service.change_privacy_settings(
                user_id=command.user_id,
                new_privacy_settings=command.new_privacy_settings
            )
            await self.event_bus.process_events(user)
            return {
                "success": True,
                "user_id": command.user_id,
                "new_privacy_settings": command.new_privacy_settings
            }

        except Exception as e:
            return {
                "success": False,
                "exception": str(e)
            }
