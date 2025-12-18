from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from LuminUserService.app.domain.models.aggregates.aggregate_root import AggregateRoot
from LuminUserService.app.domain.models.entities.profile_view import ProfileView
from LuminUserService.app.domain.models.common.value_objects import Username, Date, Email, Bio, UserStatus, AvatarURL, \
    PrivacySettings, PhoneNumber, LanguageCode
from LuminUserService.app.domain.events.user_events import (UserChangedUsernameEvent, UserChangedDateEvent,
                                                            UserChangedEmailEvent, UserChangedLanguageCodeEvent,
                                                            UserChangedBioEvent, UserChangedAvatarURLEvent,
                                                            UserChangedPrivacySettingsEvent, UserBlockedEvent,
                                                            UserActivatedEvent, UserDeactivatedEvent, UserChangedPhoneEvent)


@dataclass
class User(AggregateRoot):
    def __init__(
        self,
        user_id: UUID = uuid4(),
        username: Username = field(default_factory=Username),
        date: Date | None = None,
        phone: PhoneNumber = field(default_factory=PhoneNumber),
        email: Email | None = None,
        language_code: LanguageCode = field(default_factory=LanguageCode),
        bio: Bio | None = None,
        avatar_url: AvatarURL = field(default_factory=AvatarURL),
        privacy_settings: PrivacySettings = field(default_factory=PrivacySettings),
        profile_views: list[ProfileView] = None,
        status: str = UserStatus.ACTIVE
    ) -> None:
        super().__init__(user_id)

        self.username: Username = username
        self.date: Date = date
        self.phone = phone
        self.email: Email = email
        self.language_code: LanguageCode = language_code
        self.bio: Bio = bio
        self.avatar_url: AvatarURL = avatar_url
        self.privacy_settings: PrivacySettings = privacy_settings

        if profile_views is None:
            profile_views = field(default_factory=list)

        self.profile_views = profile_views
        self.status: str = status

    def change_username(self, new_username: Username) -> None:
        self.username: Username = new_username
        self.add_domain_event(UserChangedUsernameEvent(
            user_id=super().id,
            new_username=new_username
        ))
        self._increment_version()

    def change_date(self, new_date: Date) -> None:
        self.date: Date = new_date
        self.add_domain_event(UserChangedDateEvent(
            user_id=super().id,
            new_date=new_date
        ))
        self._increment_version()

    def change_email(self, new_email: Email) -> None:
        self.email: Email = new_email
        self.add_domain_event(UserChangedEmailEvent(
            user_id=super().id,
            new_email=new_email
        ))
        self._increment_version()

    def change_phone(self, new_phone: PhoneNumber) -> None:
        self.phone: PhoneNumber = new_phone
        self.add_domain_event(UserChangedPhoneEvent(
            user_id=super().id,
            new_phone=new_phone
        ))
        self._increment_version()

    def change_language_code(self, new_language_code: LanguageCode) -> None:
        self.language_code: LanguageCode = new_language_code
        self.add_domain_event(UserChangedLanguageCodeEvent(
            user_id=super().id,
            new_language_code=new_language_code
        ))
        self._increment_version()

    def change_bio(self, new_bio: Bio) -> None:
        self.bio: Bio = new_bio
        self.add_domain_event(UserChangedBioEvent(
            user_id=super().id,
            new_bio=new_bio
        ))
        self._increment_version()

    def change_avatar_url(self, new_avatar_url: AvatarURL) -> None:
        self.avatar_url: AvatarURL = new_avatar_url
        self.add_domain_event(UserChangedAvatarURLEvent(
            user_id=super().id,
            new_avatar_url=new_avatar_url
        ))
        self._increment_version()

    def change_privacy_settings(self, new_privacy_settings: PrivacySettings):
        self.privacy_settings: PrivacySettings = new_privacy_settings
        self.add_domain_event(UserChangedPrivacySettingsEvent(
            user_id=super().id,
            new_privacy_settings=new_privacy_settings
        ))
        self._increment_version()

    def record_profile_view(self, view_id: UUID, viewer_id: UUID, viewer_ip: str) -> None:
        view: ProfileView = ProfileView(
            view_id=view_id,
            viewer_id=viewer_id,
            view_ip=viewer_ip,
            viewed_at=datetime.now()
        )
        self.profile_views.append(view)
        self._increment_version()

    def block(self) -> None:
        self.status: str = UserStatus.BLOCKED
        self.add_domain_event(UserBlockedEvent(user_id=super().id))
        self._increment_version()

    def activate(self) -> None:
        self.status: str = UserStatus.ACTIVE
        self.add_domain_event(UserActivatedEvent(user_id=super().id))
        self._increment_version()

    def deactivate(self) -> None:
        self.status: str = UserStatus.INACTIVE
        self.add_domain_event(UserDeactivatedEvent(user_id=super().id))
        self._increment_version()
