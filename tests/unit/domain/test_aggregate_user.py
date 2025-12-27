import datetime
import pytest
from uuid import uuid4
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import (
    Username, Date, Email, Bio, AvatarURL,
    PrivacySettings, PhoneNumber, LanguageCode
)
from LuminUserService.app.domain.events.user_events import (
    UserCreatedEvent,
    UserActivatedEvent,
    UserBlockedEvent,
    UserDeactivatedEvent,
    UserChangedUsernameEvent, UserChangedEmailEvent, UserChangedPhoneEvent,
)


class TestUserAggregate:
    @pytest.fixture
    def user(self):
        return User(
            user_id=uuid4(),
            username=Username(first_name="John", last_name="Doe"),
            date=Date(value=datetime.datetime.now()),
            phone=PhoneNumber(value="+1234567890"),
            email=Email(value="john.doe@example.com"),
            language_code=LanguageCode(value="en"),
            bio=Bio(value="Software Developer"),
            avatar_url=AvatarURL(value="https://example.com/avatar.jpg"),
            privacy_settings=PrivacySettings(),
            profile_views=[],
            status="active"
        )

    def test_create_user(self, user):
        assert user.id is not None
        assert user.username.first_name == "John"
        assert user.username.last_name == "Doe"
        assert user.status == "active"

        events = user.get_domain_events()
        assert len(events) == 1
        assert isinstance(events[0], UserCreatedEvent)

    def test_change_username(self, user):
        old_username = user.username

        user.change_username(
            Username("Jane", "Smith")
        )

        assert user.username.first_name == "Jane"
        assert user.username.last_name == "Smith"
        assert user.username != old_username

        events = user.get_domain_events()
        assert any(isinstance(event, UserChangedUsernameEvent) for event in events)

    def test_change_email(self, user):
        old_email = user.email

        user.change_email(Email("jane.smith@example.com"))

        assert user.email.value == "jane.smith@example.com"
        assert user.email != old_email

        events = user.get_domain_events()
        assert any(isinstance(event, UserChangedEmailEvent) for event in events)

    def test_change_phone(self, user):
        old_phone = user.phone

        user.change_phone(PhoneNumber("+0987654321"))

        assert user.phone.value == "+0987654321"
        assert user.phone != old_phone

        events = user.get_domain_events()
        assert any(isinstance(event, UserChangedPhoneEvent) for event in events)

    def test_activate_user(self, user):
        user.deactivate()
        user.clear_domain_events()

        user.activate()

        assert user.status == "active"

        events = user.get_domain_events()
        assert any(isinstance(event, UserActivatedEvent) for event in events)

    def test_deactivate_user(self, user):
        user.deactivate()

        assert user.status == "inactive"

        events = user.get_domain_events()
        assert any(isinstance(event, UserDeactivatedEvent) for event in events)

    def test_block_user(self, user):
        user.block()

        assert user.status == "blocked"

        events = user.get_domain_events()
        assert any(isinstance(event, UserBlockedEvent) for event in events)

    def test_version_increment_on_change(self, user):
        initial_version = user.version

        user.change_username(Username("Jane", "Smith"))
        assert user.version == initial_version + 1

        user.change_email(Email("jane.smith@example.com"))
        assert user.version == initial_version + 2

    def test_clear_domain_events(self, user):
        user.change_username(Username("Jane", "Smith"))
        user.change_email(Email("jane.smith@example.com"))

        assert len(user.get_domain_events()) == 3

        user.clear_domain_events()
        assert len(user.get_domain_events()) == 0
