from uuid import UUID, uuid4
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class UsernameModel(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)


class ProfileViewModel(BaseModel):
    viewer_id: str
    viewer_ip: str
    viewed_at: str


class PrivacySettingsModel(BaseModel):
    profile_avatar_visibility_for_contacts: bool = True
    profile_avatar_visibility_for_all_users: bool = True
    profile_avatar_visibility_black_list: list[UUID] = []
    profile_avatar_visibility_white_list: list[UUID] = []

    profile_date_of_born_visibility_for_contacts: bool = True
    profile_date_of_born_visibility_for_all_users: bool = True
    profile_date_of_born_visibility_black_list: list[UUID] = []
    profile_date_of_born_visibility_white_list: list[UUID] = []

    profile_phone_number_visibility_for_contacts: bool = True
    profile_phone_number_visibility_for_all_users: bool = True
    profile_phone_number_visibility_black_list: list[UUID] = []
    profile_phone_number_visibility_white_list: list[UUID] = []

    profile_email_address_visibility_for_contacts: bool = True
    profile_email_address_visibility_for_all_users: bool = True
    profile_email_address_visibility_black_list: list[UUID] = []
    profile_email_address_visibility_white_list: list[UUID] = []


class CreateUserRequest(BaseModel):
    user_id: UUID = uuid4()
    username: UsernameModel
    date: str
    phone: str
    email: Optional[str] = None
    language_code: str = Field(..., min_length=2, max_length=10)
    bio: Optional[str] = None
    avatar_url: str
    privacy_settings: PrivacySettingsModel
    profile_views: Optional[List[ProfileViewModel]] = []

    @validator('phone')
    def validate_phone(cls, v):
        if not v.startswith('+'):
            raise ValueError('Phone number must start with +')
        if len(v) < 10:
            raise ValueError('Phone number too short')
        return v

    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            raise ValueError('date must be in ISO format')


class PrivacySettingsUpdate(BaseModel):
    profile_avatar_visibility_for_contacts: bool
    profile_avatar_visibility_for_all_users: bool
    profile_avatar_visibility_black_list: List[str] = []
    profile_avatar_visibility_white_list: List[str] = []

    profile_date_of_born_visibility_for_contacts: bool
    profile_date_of_born_visibility_for_all_users: bool
    profile_date_of_born_visibility_black_list: List[str] = []
    profile_date_of_born_visibility_white_list: List[str] = []

    profile_phone_number_visibility_for_contacts: bool
    profile_phone_number_visibility_for_all_users: bool
    profile_phone_number_visibility_black_list: List[str] = []
    profile_phone_number_visibility_white_list: List[str] = []

    profile_email_address_visibility_for_contacts: bool
    profile_email_address_visibility_for_all_users: bool
    profile_email_address_visibility_black_list: List[str] = []
    profile_email_address_visibility_white_list: List[str] = []
