from datetime import datetime
from uuid import uuid4

import factory
from factory import Factory

from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.models.common.value_objects import Username, Date, Email, Bio, AvatarURL, PhoneNumber, \
    LanguageCode, PrivacySettings


class UsernameFactory(Factory):
    class Meta:
        model = Username

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class DateFactory(Factory):
    class Meta:
        model = Date

    value = factory.Faker("value")


class EmailFactory(Factory):
    class Meta:
        model = Email

    value = factory.Faker("value")


class BioFactory(Factory):
    class Meta:
        model = Bio

    value = factory.Faker("value")


class AvatarURLFactory(Factory):
    class Meta:
        model = AvatarURL

    value = factory.Faker("value")


class PhoneNumberFactory(Factory):
    class Meta:
        model = PhoneNumber

    value = factory.Faker("value")


class LanguageCodeFactory(Factory):
    class Meta:
        model = LanguageCode

    value = factory.Faker("value")


class PrivacySettingsFactory(Factory):
    class Meta:
        model = PrivacySettings

    profile_avatar_visibility_for_contacts: bool = True
    profile_avatar_visibility_for_all_users: bool = True
    profile_avatar_visibility_black_list: list = factory.LazyFunction(list)
    profile_avatar_visibility_white_list: list = factory.LazyFunction(list)

    profile_date_of_born_visibility_for_contacts: bool = True
    profile_date_of_born_visibility_for_all_users: bool = True
    profile_date_of_born_visibility_black_list: list = factory.LazyFunction(list)
    profile_date_of_born_visibility_white_list: list = factory.LazyFunction(list)

    profile_phone_number_visibility_for_contacts: bool = True
    profile_phone_number_visibility_for_all_users: bool = True
    profile_phone_number_visibility_black_list: list = factory.LazyFunction(list)
    profile_phone_number_visibility_white_list: list = factory.LazyFunction(list)

    profile_email_address_visibility_for_contacts: bool = True
    profile_email_address_visibility_for_all_users: bool = True
    profile_email_address_visibility_black_list: list = factory.LazyFunction(list)
    profile_email_address_visibility_white_list: list = factory.LazyFunction(list)


class UserFactory(Factory):
    class Meta:
        model = User

    id = factory.LazyFunction(uuid4)
    username = factory.SubFactory(UsernameFactory)
    date = factory.SubFactory(DateFactory)
    phone = factory.SubFactory(PhoneNumberFactory)
    email = factory.SubFactory(EmailFactory)
    language_code = factory.SubFactory(LanguageCodeFactory)
    bio = factory.SubFactory(BioFactory)
    avatar_url = factory.SubFactory(AvatarURLFactory)
    privacy_settings = factory.SubFactory(PrivacySettingsFactory)
    profile_views = factory.LazyFunction(list)
    status = "active"
    version = 1


class ActiveUserFactory(UserFactory):
    status = "active"


class InactiveUserFactory(UserFactory):
    status = "inactive"


class BlockedUserFactory(UserFactory):
    status = "blocked"


class UserWithProfileViewsFactory(UserFactory):
    profile_views = factory.LazyAttribute(lambda _: [
        {
            "view_id": uuid4(),
            "viewer_id": uuid4(),
            "view_ip": factory.Faker('ipv4'),
            "viewed_at": datetime.utcnow()
        }
        for _ in range(3)
    ])
