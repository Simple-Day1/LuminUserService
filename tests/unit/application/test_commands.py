import datetime
import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from LuminUserService.app.application.commands.create import CreateUserCommand, CreateUserHandler
from LuminUserService.app.application.commands.change_username import ChangeUsernameCommand, ChangeUsernameHandler
from LuminUserService.app.application.commands.change_email import ChangeEmailCommand, ChangeEmailHandler
from LuminUserService.app.application.commands.change_phone import ChangePhoneCommand, ChangePhoneHandler
from LuminUserService.app.domain.models.common.value_objects import Username, PhoneNumber, Date, Email, LanguageCode, \
    Bio, AvatarURL, PrivacySettings


class TestCommandHandlers:
    @pytest.fixture
    def mock_user_service(self, mocker):
        mock = mocker.AsyncMock()
        mock.create_user = mocker.AsyncMock()
        mock.change_username = mocker.AsyncMock()
        mock.change_email = mocker.AsyncMock()
        mock.change_phone = mocker.AsyncMock()
        return mock

    @pytest.fixture
    def mock_event_bus(self):
        return AsyncMock()

    @pytest.mark.asyncio
    async def test_create_user_handler(self, mock_user_service, mock_event_bus):
        handler = CreateUserHandler(mock_user_service, mock_event_bus)

        command = CreateUserCommand(
            user_id=uuid4(),
            username=Username("John", "Doe"),
            date=Date(datetime.datetime.now()),
            phone=PhoneNumber("+1234567890"),
            email=Email("john.doe@example.com"),
            language_code=LanguageCode("en"),
            bio=Bio("Developer"),
            avatar_url=AvatarURL("https://example.com/avatar.jpg"),
            privacy_settings=PrivacySettings(),
            profile_views=[]
        )

        result = await handler.handle(command)

        mock_user_service.create_user.assert_called_once_with(
            user_id=command.user_id,
            username=command.username,
            date=command.date,
            phone=command.phone,
            email=command.email,
            language_code=command.language_code,
            bio=command.bio,
            avatar_url=command.avatar_url,
            privacy_settings=command.privacy_settings,
            profile_views=command.profile_views
        )
        mock_event_bus.process_events.assert_called_once()
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_change_username_handler(self, mock_user_service, mock_event_bus):
        handler = ChangeUsernameHandler(mock_user_service, mock_event_bus)

        user_id = uuid4()
        command = ChangeUsernameCommand(
            user_id=user_id,
            new_username=Username("Jane", "Smith")
        )

        result = await handler.handle(command)

        mock_user_service.change_username.assert_called_once_with(
            user_id=command.user_id,
            new_username=command.new_username
        )
        mock_event_bus.process_events.assert_called_once()
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_change_email_handler(self, mock_user_service, mock_event_bus):
        handler = ChangeEmailHandler(mock_user_service, mock_event_bus)

        user_id = uuid4()
        command = ChangeEmailCommand(
            user_id=user_id,
            new_email=Email("jane.smith@example.com")
        )

        result = await handler.handle(command)

        mock_user_service.change_email.assert_called_once_with(
            user_id=command.user_id,
            new_email=command.new_email
        )
        mock_event_bus.process_events.assert_called_once()
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_change_phone_handler(self, mock_user_service, mock_event_bus):
        handler = ChangePhoneHandler(mock_user_service, mock_event_bus)

        user_id = uuid4()
        command = ChangePhoneCommand(
            user_id=user_id,
            new_phone=PhoneNumber("+0987654321")
        )

        result = await handler.handle(command)

        mock_user_service.change_phone.assert_called_once_with(
            user_id=command.user_id,
            new_phone=command.new_phone
        )
        mock_event_bus.process_events.assert_called_once()
        assert result["success"] is True

    @pytest.mark.asyncio
    async def test_handler_with_service_error(self, mock_user_service, mock_event_bus):
        handler = CreateUserHandler(mock_user_service, mock_event_bus)
        mock_user_service.create_user.side_effect = Exception("Service error")

        command = CreateUserCommand(
            user_id=uuid4(),
            username=Username("John", "Doe"),
            date=Date(datetime.datetime.now()),
            phone=PhoneNumber("+1234567890"),
            email=Email("john.doe@example.com"),
            language_code=LanguageCode("en"),
            bio=Bio("Developer"),
            avatar_url=AvatarURL("https://example.com/avatar.jpg"),
            privacy_settings=PrivacySettings(),
            profile_views=[]
        )

        result = await handler.handle(command)

        assert result["success"] is False
        assert "Service error" in result["exception"]
