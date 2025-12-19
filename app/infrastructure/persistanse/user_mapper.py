from typing import Any
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.entities.profile_view import ProfileView
from LuminUserService.app.domain.repositories.data_mapper import UserDataMapper
from LuminUserService.app.domain.models.common.value_objects import (
    Username, Date, Email, Bio, AvatarURL,
    PrivacySettings, PhoneNumber, LanguageCode
)


class UserMapper(UserDataMapper):
    def to_domain(self, data: dict) -> User:
        try:
            username = Username(
                first_name=data["first_name"],
                last_name=data["last_name"]
            )

            date = Date(value=data["date"]) if data["date"] else None
            email = Email(value=data["email"]) if data["email"] else None
            bio = Bio(value=data["bio"]) if data["bio"] else None
            avatar_url = AvatarURL(value=data["avatar_url"])
            phone = PhoneNumber(value=data["phone"])
            language_code_value = data["language_code"]

            if isinstance(language_code_value, str) and language_code_value.startswith('LanguageCode'):
                import re
                match = re.search(r"'([^']+)'", language_code_value)
                if match:
                    language_code_value = match.group(1)

            language_code = LanguageCode(value=language_code_value)

            privacy_settings = PrivacySettings(
                profile_avatar_visibility_for_contacts=data["profile_avatar_visibility_for_contacts"],
                profile_avatar_visibility_for_all_users=data["profile_avatar_visibility_for_all_users"],
                profile_avatar_visibility_black_list=data["profile_avatar_visibility_black_list"] or [],
                profile_avatar_visibility_white_list=data["profile_avatar_visibility_white_list"] or [],
                profile_date_of_born_visibility_for_contacts=data["profile_date_of_born_visibility_for_contacts"],
                profile_date_of_born_visibility_for_all_users=data["profile_date_of_born_visibility_for_all_users"],
                profile_date_of_born_visibility_black_list=data["profile_date_of_born_visibility_black_list"] or [],
                profile_date_of_born_visibility_white_list=data["profile_date_of_born_visibility_white_list"] or [],
                profile_phone_number_visibility_for_contacts=data["profile_phone_number_visibility_for_contacts"],
                profile_phone_number_visibility_for_all_users=data["profile_phone_number_visibility_for_all_users"],
                profile_phone_number_visibility_black_list=data["profile_phone_number_visibility_black_list"] or [],
                profile_phone_number_visibility_white_list=data["profile_phone_number_visibility_white_list"] or [],
                profile_email_address_visibility_for_contacts=data["profile_email_address_visibility_for_contacts"],
                profile_email_address_visibility_for_all_users=data["profile_email_address_visibility_for_all_users"],
                profile_email_address_visibility_black_list=data["profile_email_address_visibility_black_list"] or [],
                profile_email_address_visibility_white_list=data["profile_email_address_visibility_white_list"] or [],
            )

            profile_views = []
            if data["profile_views"]:
                for view_data in data["profile_views"]:
                    profile_views.append(ProfileView(
                        view_id=view_data["view_id"],
                        viewer_id=view_data["viewer_id"],
                        view_ip=view_data["view_ip"],
                        viewed_at=view_data["viewed_at"]
                    ))

            user = User(
                user_id=data["user_id"],
                username=username,
                date=date,
                phone=phone,
                email=email,
                language_code=language_code,
                bio=bio,
                avatar_url=avatar_url,
                privacy_settings=privacy_settings,
                profile_views=profile_views,
                status=data["status"]
            )

            return user

        except Exception as e:
            raise ValueError(f"Error mapping to domain: {e}")

    def to_persistence(self, user: User) -> dict[str, Any]:
        try:
            profile_views_data = []
            for view in user.profile_views:
                profile_views_data.append({
                    "view_id": view.view_id,
                    "viewer_id": view.viewer_id,
                    "view_ip": view.view_ip,
                    "viewed_at": view.viewed_at.isoformat() if hasattr(view.viewed_at, 'isoformat') else view.viewed_at
                })

            return {
                "user_id": user.id,
                "first_name": user.username.first_name,
                "last_name": user.username.last_name,
                "date": user.date.value if user.date.value else None,
                "phone": str(user.phone.value),
                "email": str(user.email.value) if user.email else None,
                "language_code": str(user.language_code.value),
                "bio": str(user.bio.value) if user.bio.value else None,
                "avatar_url": str(user.avatar_url.value),
                "profile_avatar_visibility_for_contacts":
                    user.privacy_settings.profile_avatar_visibility_for_contacts,
                "profile_avatar_visibility_for_all_users":
                    user.privacy_settings.profile_avatar_visibility_for_all_users,
                "profile_avatar_visibility_black_list":
                    user.privacy_settings.profile_avatar_visibility_black_list,
                "profile_avatar_visibility_white_list":
                    user.privacy_settings.profile_avatar_visibility_white_list,
                "profile_date_of_born_visibility_for_contacts":
                    user.privacy_settings.profile_date_of_born_visibility_for_contacts,
                "profile_date_of_born_visibility_for_all_users":
                    user.privacy_settings.profile_date_of_born_visibility_for_all_users,
                "profile_date_of_born_visibility_black_list":
                    user.privacy_settings.profile_date_of_born_visibility_black_list,
                "profile_date_of_born_visibility_white_list":
                    user.privacy_settings.profile_date_of_born_visibility_white_list,
                "profile_phone_number_visibility_for_contacts":
                    user.privacy_settings.profile_phone_number_visibility_for_contacts,
                "profile_phone_number_visibility_for_all_users":
                    user.privacy_settings.profile_phone_number_visibility_for_all_users,
                "profile_phone_number_visibility_black_list":
                    user.privacy_settings.profile_phone_number_visibility_black_list,
                "profile_phone_number_visibility_white_list":
                    user.privacy_settings.profile_phone_number_visibility_white_list,
                "profile_email_address_visibility_for_contacts":
                    user.privacy_settings.profile_email_address_visibility_for_contacts,
                "profile_email_address_visibility_for_all_users":
                    user.privacy_settings.profile_email_address_visibility_for_all_users,
                "profile_email_address_visibility_black_list":
                    user.privacy_settings.profile_email_address_visibility_black_list,
                "profile_email_address_visibility_white_list":
                    user.privacy_settings.profile_email_address_visibility_white_list,
                "profile_views": profile_views_data,
                "status": user.status,
                "version": user.version
            }
        except Exception as e:
            raise ValueError(f"Error mapping to persistence: {e}")

    def to_domain_list(self, data_list: list[dict]) -> list[User]:
        return [self.to_domain(data) for data in data_list]
