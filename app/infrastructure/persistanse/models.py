import uuid
from sqlalchemy import Column, UUID, String, Date, Boolean, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(UUID(), primary_key=True, default=lambda: uuid.uuid4())
    first_name = Column(String(30))
    last_name = Column(String(30))
    date = Column(Date(), nullable=True)
    phone = Column(String(30), unique=True, nullable=True)
    email = Column(String(30), unique=True, nullable=True)
    language_code = Column(String(10))
    bio = Column(String(100), nullable=True)
    avatar_url = Column(String(100))
    profile_avatar_visibility_for_contacts = Column(Boolean())
    profile_avatar_visibility_for_all_users = Column(Boolean())
    profile_avatar_visibility_black_list = Column(JSON())
    profile_avatar_visibility_white_list = Column(JSON())
    profile_date_of_born_visibility_for_contacts = Column(Boolean())
    profile_date_of_born_visibility_for_all_users = Column(Boolean())
    profile_date_of_born_visibility_black_list = Column(JSON())
    profile_date_of_born_visibility_white_list = Column(JSON())
    profile_phone_number_visibility_for_contacts = Column(Boolean())
    profile_phone_number_visibility_for_all_users = Column(Boolean())
    profile_phone_number_visibility_black_list = Column(JSON())
    profile_phone_number_visibility_white_list = Column(JSON())
    profile_email_address_visibility_for_contacts = Column(Boolean())
    profile_email_address_visibility_for_all_users = Column(Boolean())
    profile_email_address_visibility_black_list = Column(JSON())
    profile_email_address_visibility_white_list = Column(JSON())
    profile_views = Column(JSON)
    status = Column(String(30))
    version = Column(Integer())
