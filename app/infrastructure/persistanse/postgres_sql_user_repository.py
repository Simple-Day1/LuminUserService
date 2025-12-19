from uuid import UUID
from psycopg2.extras import RealDictCursor
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.repositories.reposiotries import UserRepository
from LuminUserService.app.infrastructure.cache.multi_level_cache import MultiLevelCache
from LuminUserService.app.infrastructure.persistanse.identity_map import UserIdentityMap
from LuminUserService.app.infrastructure.persistanse.user_mapper import UserMapper


class PostgresSQLUserRepository(UserRepository):
    def __init__(self, connection_factory, identity_map: UserIdentityMap, cache: MultiLevelCache) -> None:
        self.connection_factory = connection_factory
        self.identity_map = identity_map
        self.mapper = UserMapper()
        self.cache = cache

    def _get_connection(self):
        conn = self.connection_factory()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cursor

    async def save(self, user: User) -> None:
        print(f"Saving user {user.id}")
        print("=" * 50)
        print("DATA BEING SAVED TO DATABASE:")
        print(f"  user.id: {user.id}")
        print(f"  user.username.first_name: '{user.username.first_name}' (length: {len(user.username.first_name)})")
        print(f"  user.username.last_name: '{user.username.last_name}' (length: {len(user.username.last_name)})")
        print(f"  user.date.value: {user.date.value if user.date else None}")
        print(f"  user.phone.value: '{user.phone.value}' (length: {len(user.phone.value)})")
        print(f"  user.email.value: '{user.email.value if user.email else None}'")
        print(f"  user.language_code: '{str(user.language_code)}' (length: {len(str(user.language_code))})")
        print(f"  user.bio.value: '{user.bio.value if user.bio else None}'")
        print(f"  user.avatar_url: '{str(user.avatar_url)}'")
        print(f"  user.privacy_settings: '{user.privacy_settings}'")
        print(f"  user.status: '{user.status}' (length: {len(user.status)})")
        print("=" * 50)

        field_lengths = {
            "first_name": len(user.username.first_name),
            "last_name": len(user.username.last_name),
            "phone": len(user.phone.value),
            "language_code": len(str(user.language_code)),
            "status": len(user.status),
        }

        print("Field lengths:")
        for field, length in field_lengths.items():
            print(f"  {field}: {length} chars")

        problematic_fields = {k: v for k, v in field_lengths.items() if v > 10}
        if problematic_fields:
            print(f"WARNING: Fields longer than 10 chars: {problematic_fields}")

        def get_language_code_value(obj):
            if hasattr(obj, 'value'):
                return obj.value
            elif isinstance(obj, str):
                if obj.startswith('LanguageCode'):
                    import re
                    match = re.search(r"'([^']+)'", obj)
                    if match:
                        return match.group(1)
                return obj
            else:
                return str(obj)

        language_code_value = get_language_code_value(user.language_code)
        print(f"✅ Clean language_code: '{language_code_value}' (length: {len(language_code_value)})")

        conn, cursor = self._get_connection()

        try:
            check_sql = "SELECT user_id FROM users WHERE user_id = %s"
            cursor.execute(check_sql, (str(user.id),))
            existing_user = cursor.fetchone()

            if existing_user:
                update_sql = """
                UPDATE users SET
                    first_name = %s,
                    last_name = %s,
                    date = %s,
                    phone = %s,
                    email = %s,
                    language_code = %s,
                    bio = %s,
                    avatar_url = %s,
                    profile_avatar_visibility_for_contacts = %s,
                    profile_avatar_visibility_for_all_users = %s,
                    profile_avatar_visibility_black_list = %s,
                    profile_avatar_visibility_white_list = %s,
                    profile_date_of_born_visibility_for_contacts = %s,
                    profile_date_of_born_visibility_for_all_users = %s,
                    profile_date_of_born_visibility_black_list = %s,
                    profile_date_of_born_visibility_white_list = %s,
                    profile_phone_number_visibility_for_contacts = %s,
                    profile_phone_number_visibility_for_all_users = %s,
                    profile_phone_number_visibility_black_list = %s,
                    profile_phone_number_visibility_white_list = %s,
                    profile_email_address_visibility_for_contacts = %s,
                    profile_email_address_visibility_for_all_users = %s,
                    profile_email_address_visibility_black_list = %s,
                    profile_email_address_visibility_white_list = %s,
                    status = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s
                """

                user_data = (
                    user.username.first_name,
                    user.username.last_name,
                    user.date.value if user.date else None,
                    user.phone.value,
                    user.email.value if user.email else None,
                    language_code_value,
                    user.bio.value if user.bio else None,
                    str(user.avatar_url),
                    user.privacy_settings.profile_avatar_visibility_for_contacts,
                    user.privacy_settings.profile_avatar_visibility_for_all_users,
                    user.privacy_settings.profile_avatar_visibility_black_list,
                    user.privacy_settings.profile_avatar_visibility_white_list,
                    user.privacy_settings.profile_date_of_born_visibility_for_contacts,
                    user.privacy_settings.profile_date_of_born_visibility_for_all_users,
                    user.privacy_settings.profile_date_of_born_visibility_black_list,
                    user.privacy_settings.profile_date_of_born_visibility_white_list,
                    user.privacy_settings.profile_phone_number_visibility_for_contacts,
                    user.privacy_settings.profile_phone_number_visibility_for_all_users,
                    user.privacy_settings.profile_phone_number_visibility_black_list,
                    user.privacy_settings.profile_phone_number_visibility_white_list,
                    user.privacy_settings.profile_email_address_visibility_for_contacts,
                    user.privacy_settings.profile_email_address_visibility_for_all_users,
                    user.privacy_settings.profile_email_address_visibility_black_list,
                    user.privacy_settings.profile_email_address_visibility_white_list,
                    user.status,
                    str(user.id)
                )

                cursor.execute(update_sql, user_data)
                print(f"User updated: {user.id}")

            else:
                insert_sql = """
                INSERT INTO users (
                    user_id, 
                    first_name, 
                    last_name, 
                    date, 
                    phone, 
                    email,
                    language_code, 
                    bio, 
                    avatar_url, 
                    status, 
                    created_at, 
                    profile_avatar_visibility_for_contacts, 
                    profile_avatar_visibility_for_all_users,
                    profile_avatar_visibility_black_list,
                    profile_avatar_visibility_white_list,
                    profile_date_of_born_visibility_for_contacts,
                    profile_date_of_born_visibility_for_all_users,
                    profile_date_of_born_visibility_black_list,
                    profile_date_of_born_visibility_white_list,
                    profile_phone_number_visibility_for_contacts,
                    profile_phone_number_visibility_for_all_users,
                    profile_phone_number_visibility_black_list,
                    profile_phone_number_visibility_white_list,
                    profile_email_address_visibility_for_contacts,
                    profile_email_address_visibility_for_all_users,
                    profile_email_address_visibility_black_list,
                    profile_email_address_visibility_white_list,
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s CURRENT_TIMESTAMP)
                """

                user_data = (
                    str(user.id),
                    user.username.first_name,
                    user.username.last_name,
                    user.date.value if user.date else None,
                    user.phone.value,
                    user.email.value if user.email else None,
                    str(user.language_code),
                    user.bio.value if user.bio else None,
                    str(user.avatar_url),
                    user.status
                )

                cursor.execute(insert_sql, user_data)
                print(f"User created: {user.id}")

            conn.commit()

            await self.cache.invalidate_user(user.id)
            user_dict = self.mapper.to_persistence(user)
            await self.cache.set_user(user.id, user_dict)

        except Exception as e:
            conn.rollback()
            await self.cache.invalidate_user(user.id)
            print(f"Error saving user {user.id}: {e}")
            raise

        finally:
            cursor.close()
            conn.close()

        self.identity_map.add(user)
        user.clear_domain_events()

    async def get_by_id(self, user_id: UUID) -> User | None:
        cached_user = await self.cache.get_user(user_id)

        if cached_user:
            print(f"User {user_id} found in cache")
            return cached_user

        conn, cursor = self._get_connection()

        try:
            select_sql = """
            SELECT 
                user_id,
                first_name,
                last_name,
                date,
                phone,
                email,
                language_code,
                bio,
                avatar_url,
                status,
                profile_avatar_visibility_for_contacts,
                profile_avatar_visibility_for_all_users,
                profile_avatar_visibility_black_list,
                profile_avatar_visibility_white_list,
                profile_date_of_born_visibility_for_contacts,
                profile_date_of_born_visibility_for_all_users,
                profile_date_of_born_visibility_black_list,
                profile_date_of_born_visibility_white_list,
                profile_phone_number_visibility_for_contacts,
                profile_phone_number_visibility_for_all_users,
                profile_phone_number_visibility_black_list,
                profile_phone_number_visibility_white_list,
                profile_email_address_visibility_for_contacts,
                profile_email_address_visibility_for_all_users,
                profile_email_address_visibility_black_list,
                profile_email_address_visibility_white_list,
                profile_views
            FROM users 
            WHERE user_id = %s
            """

            cursor.execute(select_sql, (str(user_id),))
            user_data = cursor.fetchone()

            if not user_data:
                return None

            user_dict = dict(user_data)

            print(user_dict)

            user = self.mapper.to_domain(user_dict)
            await self.cache.set_user(user_id, user_dict)
            self.identity_map.add(user)

            return user

        except Exception as e:
            print(f"Error getting user {user_id}: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    async def delete(self, user_id: UUID) -> None:
        conn, cursor = self._get_connection()

        try:
            delete_sql = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(delete_sql, (str(user_id),))
            conn.commit()

            await self.cache.invalidate_user(user_id)
            self.identity_map.remove(user_id)

            print(f"User {user_id} deleted from database and cache")

        except Exception as e:
            conn.rollback()
            print(f"Error deleting user {user_id}: {e}")
            raise

        finally:
            cursor.close()
            conn.close()
