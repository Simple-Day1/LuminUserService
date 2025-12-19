import logging
from datetime import datetime
from taskiq import TaskiqDepends
from uuid import UUID
from LuminUserService.app.application.commands.activate import ActivateCommand
from LuminUserService.app.application.commands.block import BlockCommand
from LuminUserService.app.application.commands.change_avatar_url import ChangeAvatarURLCommand
from LuminUserService.app.application.commands.change_bio import ChangeBioCommand
from LuminUserService.app.application.commands.change_date import ChangeDateCommand
from LuminUserService.app.application.commands.change_email import ChangeEmailCommand
from LuminUserService.app.application.commands.change_language_code import ChangeLanguageCodeCommand
from LuminUserService.app.application.commands.change_phone import ChangePhoneCommand
from LuminUserService.app.application.commands.change_privacy_settings import ChangePrivacySettingsCommand
from LuminUserService.app.application.commands.change_username import ChangeUsernameCommand
from LuminUserService.app.application.commands.create import CreateUserCommand
from LuminUserService.app.application.commands.deactivate import DeactivateCommand
from LuminUserService.app.application.commands.delete import DeleteCommand
from LuminUserService.app.application.commands.record_profile_view import RecordProfileViewCommand
from LuminUserService.app.application.queries.get_by_id import GetUserByIdQuery
from LuminUserService.app.infrastructure.dependency_container import DependencyContainer
from LuminUserService.app.infrastructure.persistanse.database import get_dependency_container
from LuminUserService.app.infrastructure.tasks.taskiq_broker import get_taskiq_broker
from LuminUserService.app.domain.models.common.value_objects import (
    Username, Email, PhoneNumber, Bio, AvatarURL, PrivacySettings, Date, LanguageCode
)

logger = logging.getLogger(__name__)


def get_broker():
    try:
        broker = get_taskiq_broker()
        if broker is None:
            raise RuntimeError("Taskiq broker is None")
        return broker
    except Exception as error:
        logger.error(f"Failed to get broker: {error}")
        raise


try:
    broker = get_broker()
    logger.info("Broker initialized in user_commands.py")
except Exception as e:
    logger.error(f"Failed to initialize broker: {e}")
    broker = None


if broker is not None:
    @broker.task
    async def create_user_task(
            user_data: dict,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            print("=" * 50)
            print("STARTING CREATE_USER_TASK")
            print(f"User data received: {user_data}")

            if not container:
                return {"success": False, "error": "DependencyContainer is None"}

            print("Getting create user handler...")
            create_handler = await container.get_create_user_handler()
            print(f"Create user handler obtained: {create_handler}")

            user_service = await container.get_user_service()
            print(f"User service: {user_service}")
            print(f"Connection factory: {user_service.connection_factory if user_service else 'None'}")

            print(Username(
                    first_name=user_data["username"]["first_name"],
                    last_name=user_data["username"]["last_name"]
                ))

            command = CreateUserCommand(
                user_id=user_data["user_id"],
                username=Username(
                    first_name=user_data["username"]["first_name"],
                    last_name=user_data["username"]["last_name"]
                ),
                date=Date(value=datetime.fromisoformat(user_data["date"].replace('Z', '+00:00'))),
                phone=PhoneNumber(value=user_data["phone"]),
                email=Email(value=user_data["email"]) if user_data.get("email") else None,
                language_code=LanguageCode(value=user_data["language_code"]),
                bio=Bio(value=user_data["bio"]) if user_data.get("bio") else None,
                avatar_url=AvatarURL(value=user_data["avatar_url"]),
                privacy_settings=PrivacySettings(**user_data["privacy_settings"]),
                profile_views=[]
            )

            print(f"Finishing create_user_task for user_id: {user_data["user_id"]}")
            result = await create_handler.handle(command)

            return result

        except Exception as e:
            print(f"ERROR in create_user_task: {str(e)}")
            import traceback
            print(f"📋 Traceback:\n{traceback.format_exc()}")
            return {

                "success": False,

                "error": str(e),

                "traceback": traceback.format_exc()

            }


    @broker.task
    async def change_username_task(
            user_id: str,
            new_username: dict,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_change_username_handler()

            command = ChangeUsernameCommand(
                user_id=UUID(user_id),
                new_username=Username(
                    first_name=new_username["first_name"],
                    last_name=new_username["last_name"]
                )
            )

            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "change_username"
            }


    @broker.task
    async def change_email_task(
            user_id: str,
            new_email: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_change_email_handler()

            command = ChangeEmailCommand(
                user_id=UUID(user_id),
                new_email=Email(value=new_email)
            )

            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "change_email"
            }


    @broker.task
    async def change_phone_task(
            user_id: str,
            new_phone: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_change_phone_handler()

            command = ChangePhoneCommand(
                user_id=UUID(user_id),
                new_phone=PhoneNumber(value=new_phone)
            )

            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "change_phone"
            }


    @broker.task
    async def change_bio_task(
            user_id: str,
            new_bio: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_change_bio_handler()

            command = ChangeBioCommand(
                user_id=UUID(user_id),
                new_bio=Bio(value=new_bio)
            )

            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "change_bio"
            }

    @broker.task
    async def change_date_task(
            user_id: str,
            new_date: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            print("Change date task started")
            print(f"[DEBUG] user_id: {user_id}")
            print(f"[DEBUG] new_date string: {new_date}")
            print(f"[DEBUG] new_date type: {type(new_date)}")

            try:
                print(f"[DEBUG] Attempting to parse date: {new_date}")
                parsed_date = datetime.fromisoformat(new_date.replace('Z', '+00:00'))
                print(f"[DEBUG] Parsed date: {parsed_date}")
                print(f"[DEBUG] Parsed date type: {type(parsed_date)}")
            except Exception as parse_error:
                print(f"[DEBUG] Date parsing error: {parse_error}")
                import traceback
                traceback.print_exc()
                raise

            handler = await container.get_change_date_handler()
            print("handler created")

            command = ChangeDateCommand(
                user_id=UUID(user_id),
                new_date=Date(value=parsed_date))

            print("ChangeDateCommand created")

            result = await handler.handle(command)
            print("Change date task finished")

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "change_bio"
            }


    @broker.task
    async def change_language_code_task(
            user_id: str,
            new_language_code: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_change_language_code_handler()

            command = ChangeLanguageCodeCommand(
                user_id=UUID(user_id),
                new_language_code=LanguageCode(value=new_language_code)
            )

            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "change_bio"
            }


    @broker.task
    async def change_avatar_url_task(
            user_id: str,
            new_avatar_url: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_change_avatar_url_handler()

            command = ChangeAvatarURLCommand(
                user_id=UUID(user_id),
                new_avatar_url=AvatarURL(value=new_avatar_url)
            )

            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "change_bio"
            }


    @broker.task
    async def change_privacy_settings_task(
            user_id: str,
            new_privacy_settings: dict,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            print(new_privacy_settings)
            print('Start change_privacy_settings_task')
            handler = await container.get_change_privacy_settings_handler()
            print("Handler created")

            command = ChangePrivacySettingsCommand(
                user_id=UUID(user_id),
                new_privacy_settings=PrivacySettings(
                    profile_avatar_visibility_for_contacts=bool(new_privacy_settings["profile_avatar_visibility_for_contacts"]),
                    profile_avatar_visibility_for_all_users=bool(new_privacy_settings["profile_avatar_visibility_for_all_users"]),
                    profile_avatar_visibility_black_list=list(new_privacy_settings["profile_avatar_visibility_black_list"]),
                    profile_avatar_visibility_white_list=list(new_privacy_settings["profile_avatar_visibility_white_list"]),
                    profile_date_of_born_visibility_for_contacts=bool(new_privacy_settings["profile_date_of_born_visibility_for_contacts"]),
                    profile_date_of_born_visibility_for_all_users=bool(new_privacy_settings["profile_date_of_born_visibility_for_all_users"]),
                    profile_date_of_born_visibility_black_list=list(new_privacy_settings["profile_date_of_born_visibility_black_list"]),
                    profile_date_of_born_visibility_white_list=list(new_privacy_settings["profile_date_of_born_visibility_white_list"]),
                    profile_phone_number_visibility_for_contacts=bool(new_privacy_settings["profile_phone_number_visibility_for_contacts"]),
                    profile_phone_number_visibility_for_all_users=bool(new_privacy_settings["profile_phone_number_visibility_for_all_users"]),
                    profile_phone_number_visibility_black_list=list(new_privacy_settings["profile_phone_number_visibility_black_list"]),
                    profile_phone_number_visibility_white_list=list(new_privacy_settings["profile_phone_number_visibility_white_list"]),
                    profile_email_address_visibility_for_contacts=bool(new_privacy_settings["profile_email_address_visibility_for_contacts"]),
                    profile_email_address_visibility_for_all_users=bool(new_privacy_settings["profile_email_address_visibility_for_all_users"]),
                    profile_email_address_visibility_black_list=list(new_privacy_settings["profile_email_address_visibility_black_list"]),
                    profile_email_address_visibility_white_list=list(new_privacy_settings["profile_email_address_visibility_white_list"]),
                )
            )

            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "change_bio"
            }


    @broker.task
    async def activate_user_task(
            user_id: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_activate_handler()

            command = ActivateCommand(user_id=UUID(user_id))
            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "activate_user"
            }


    @broker.task
    async def deactivate_user_task(
            user_id: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_deactivate_handler()

            command = DeactivateCommand(user_id=UUID(user_id))
            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "deactivate_user"
            }


    @broker.task
    async def block_user_task(
            user_id: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_block_handler()

            command = BlockCommand(user_id=UUID(user_id))
            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "block_user"
            }


    @broker.task
    async def record_profile_view_task(
            user_id: str,
            viewer_id: str,
            viewer_ip: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_record_profile_view_handler()

            command = RecordProfileViewCommand(
                user_id=UUID(user_id),
                viewer_id=UUID(viewer_id),
                viewer_ip=viewer_ip
            )

            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "record_profile_view"
            }


    @broker.task
    async def get_user_by_id_task(
            user_id: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            print(f"Starting get_user_by_id_task for user_id: {user_id}")
            handler = await container.get_user_by_id_handler()

            query = GetUserByIdQuery(user_id=UUID(user_id))
            result = await handler.handle(query)

            if result.get("success") and "user" in result:
                user = result["user"]

                print("🔍 Converting User object to dict...")
                from LuminUserService.app.infrastructure.persistanse.user_mapper import UserMapper
                user_dict = UserMapper().to_persistence(user)
                print(f"✅ User converted to dict: {user_dict.keys()}")

                return {
                    "success": True,
                    "user": user_dict,
                    "user_id": user_id
                }
            else:
                return {
                    "success": False,
                    "error": result.get("exception", "Unknown error"),
                    "user_id": user_id
                }

        except Exception as error:
            print(f"Error in get_user_by_id_task: {error}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(error),
                "user_id": user_id,
                "task": "get_user_by_id"
            }


    @broker.task
    async def delete_user_task(
            user_id: str,
            container: DependencyContainer = TaskiqDepends(get_dependency_container)
    ) -> dict:
        try:
            handler = await container.get_delete_user_handler()

            command = DeleteCommand(user_id=UUID(user_id))

            result = await handler.handle(command)
            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task": "change_username"
            }
