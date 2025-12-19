from uuid import UUID
from LuminUserService.app.domain.events.domain_event import DomainEvent
from LuminUserService.app.domain.models.entities.profile_view import ProfileView
from LuminUserService.app.domain.models.common.value_objects import (Username, Date, PhoneNumber, Email, LanguageCode, Bio,
                                                                     AvatarURL, PrivacySettings)


class UserCreatedEvent(DomainEvent):
    def __init__(
            self,
            user_id: UUID,
            username: Username,
            date: Date | None,
            phone: PhoneNumber,
            email: Email | None,
            language_code: LanguageCode,
            bio: Bio | None,
            avatar_url: AvatarURL,
            privacy_settings: PrivacySettings,
            profile_views: list[ProfileView]
    ) -> None:
        super().__init__(
            event_type="UserCreatedEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id,
                "username": username,
                "date": date,
                "phone": phone,
                "email": email,
                "language_code": language_code,
                "bio": bio,
                "avatar_url": avatar_url,
                "privacy_settings": privacy_settings,
                "profile_views": profile_views
            }
        )


class UserChangedUsernameEvent(DomainEvent):
    def __init__(self, user_id: UUID, new_username: Username) -> None:
        super().__init__(
            event_type="UserChangedUsernameEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id,
                "new_username": new_username,
            }
        )


class UserChangedDateEvent(DomainEvent):
    def __init__(self, user_id: UUID, new_date: Date) -> None:
        super().__init__(
            event_type="UserChangedDateEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id,
                "new_date": new_date,
            }
        )


class UserChangedEmailEvent(DomainEvent):
    def __init__(self, user_id: UUID, new_email: Email) -> None:
        super().__init__(
            event_type="UserChangedEmailEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id,
                "new_email": new_email,
            }
        )


class UserChangedPhoneEvent(DomainEvent):
    def __init__(self, user_id: UUID, new_phone: PhoneNumber) -> None:
        super().__init__(
            event_type="UserChangedPhoneEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id,
                "new_phone": new_phone,
            }
        )


class UserChangedLanguageCodeEvent(DomainEvent):
    def __init__(self, user_id: UUID, new_language_code: LanguageCode) -> None:
        super().__init__(
            event_type="UserChangedLanguageCodeEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id,
                "new_language_code": new_language_code,
            }
        )


class UserChangedBioEvent(DomainEvent):
    def __init__(self, user_id: UUID, new_bio: Bio) -> None:
        super().__init__(
            event_type="UserChangedBioEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id,
                "new_bio": new_bio,
            }
        )


class UserChangedAvatarURLEvent(DomainEvent):
    def __init__(self, user_id: UUID, new_avatar_url: AvatarURL) -> None:
        super().__init__(
            event_type="UserChangedAvatarURLEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id,
                "new_avatar_url": new_avatar_url,
            }
        )


class UserChangedPrivacySettingsEvent(DomainEvent):
    def __init__(self, user_id: UUID, new_privacy_settings: PrivacySettings) -> None:
        super().__init__(
            event_type="UserChangedPrivacySettingsEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id,
                "new_privacy_settings": new_privacy_settings,
            }
        )


class UserBlockedEvent(DomainEvent):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(
            event_type="UserBlockedEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id
            }
        )


class UserActivatedEvent(DomainEvent):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(
            event_type="UserActivatedEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id
            }
        )


class UserDeactivatedEvent(DomainEvent):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(
            event_type="UserDeactivatedEvent",
            aggregate_id=user_id,
            data={
                "user_id": user_id
            }
        )
