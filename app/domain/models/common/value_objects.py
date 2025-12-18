from uuid import UUID
from datetime import datetime
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Username:
    first_name: str
    last_name: str

    def __str__(self) -> str:
        return f"First name: {self.first_name}. Last name: {self.last_name}."


@dataclass(frozen=True)
class Date:
    value: datetime

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True)
class PhoneNumber:
    value: str

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Email:
    value: str

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Bio:
    value: str

    def __str__(self) -> str:
        return self.value


class LanguageCode:
    def __init__(self, value: str):
        if isinstance(value, str) and value.startswith('LanguageCode'):
            import re
            match = re.search(r"'([^']+)'", value)
            if match:
                value = match.group(1)

        self._value = value

    @property
    def value(self):
        return self._value

    def __str__(self):
        return self._value

    def __repr__(self):
        return f"LanguageCode('{self._value}')"


@dataclass(frozen=True)
class AvatarURL:
    value: str

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class UserStatus:
    ACTIVE: str = "active"
    INACTIVE: str = "inactive"
    BLOCKED: str = "blocked"


@dataclass(frozen=True)
class PrivacySettings:
    profile_avatar_visibility_for_contacts: bool = True
    profile_avatar_visibility_for_all_users: bool = True
    profile_avatar_visibility_black_list: list[UUID] = field(default_factory=list[UUID])
    profile_avatar_visibility_white_list: list[UUID] = field(default_factory=list[UUID])

    profile_date_of_born_visibility_for_contacts: bool = True
    profile_date_of_born_visibility_for_all_users: bool = True
    profile_date_of_born_visibility_black_list: list[UUID] = field(default_factory=list[UUID])
    profile_date_of_born_visibility_white_list: list[UUID] = field(default_factory=list[UUID])

    profile_phone_number_visibility_for_contacts: bool = True
    profile_phone_number_visibility_for_all_users: bool = True
    profile_phone_number_visibility_black_list: list[UUID] = field(default_factory=list[UUID])
    profile_phone_number_visibility_white_list: list[UUID] = field(default_factory=list[UUID])

    profile_email_address_visibility_for_contacts: bool = True
    profile_email_address_visibility_for_all_users: bool = True
    profile_email_address_visibility_black_list: list[UUID] = field(default_factory=list[UUID])
    profile_email_address_visibility_white_list: list[UUID] = field(default_factory=list[UUID])
