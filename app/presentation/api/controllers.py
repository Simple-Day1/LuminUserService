from typing import Annotated, Dict, Any
from uuid import UUID
from litestar import Controller, get, post, patch
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.params import Parameter
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from LuminUserService.app.infrastructure.persistanse.pydantic_models import CreateUserRequest, PrivacySettingsUpdate
from LuminUserService.app.infrastructure.tasks.taskiq_service import TaskiqService



def get_taskiq_service() -> TaskiqService:
    return TaskiqService()


class UserController(Controller):
    path = "/api/users"
    dependencies = {"taskiq_service": Provide(get_taskiq_service)}

    @get(
        "/{user_id:uuid}",
        summary="Get user by ID",
        description="Получить информацию о пользователе по его идентификатору",
    )
    async def get_user_by_id(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            print(f"[taskiq_handlers] Getting user by id: {user_id}")

            result = await taskiq_service.send_get_user_by_id_task(user_id)

            if result is None:
                print("[taskiq_handlers] Taskiq returned None, trying direct approach...")

                from LuminUserService.app.infrastructure.persistanse.database import get_dependency_container
                from LuminUserService.app.infrastructure.persistanse.user_mapper import UserMapper

                container = get_dependency_container()
                user_service = await container.get_user_service()
                user = await user_service.get_user_by_id(user_id)

                if not user:
                    raise HTTPException(
                        detail="User not found",
                        status_code=HTTP_404_NOT_FOUND
                    )

                return UserMapper().to_persistence(user)

            print(f"[taskiq_handlers] Taskiq result: {result}")

            if isinstance(result, dict):
                return result
            else:
                from LuminUserService.app.infrastructure.persistanse.user_mapper import UserMapper
                return result

        except ValueError as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_404_NOT_FOUND
            )
        except HTTPException:
            raise
        except Exception as e:
            print(f"[taskiq_handlers] Error: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @post(
        "/",
        summary="Create new user",
        description="Создать нового пользователя",
    )
    async def create_user(
        self,
        data: CreateUserRequest,
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            user_dict = data.dict()

            task_id = await taskiq_service.send_create_user_task(user_dict)
            return {
                "task_id": task_id,
                "status": "queued",
                "user_id": data.user_id
            }
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @patch(
        "/{user_id:uuid}/username",
        summary="Change username",
        description="Изменить имя пользователя (first name и last name)",
    )
    async def change_username(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        new_first_name: Annotated[str, Parameter(description="New first name")],
        new_last_name: Annotated[str, Parameter(description="New last name")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_change_username_task(user_id, {
                "first_name": new_first_name,
                "last_name": new_last_name
            })
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @patch(
        "/{user_id:uuid}/email",
        summary="Change email",
        description="Изменить email пользователя",
    )
    async def change_email(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        new_email: Annotated[str, Parameter(description="New email")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_change_email_task(user_id, new_email)
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @patch(
        "/{user_id:uuid}/phone",
        summary="Change phone number",
        description="Изменить номер телефона пользователя",
    )
    async def change_phone(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        new_phone: Annotated[str, Parameter(description="New phone")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_change_phone_task(user_id, new_phone)
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @patch(
        "/{user_id:uuid}/date",
        summary="Change date of birth",
        description="Изменить дату рождения пользователя",
    )
    async def change_date(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        new_date: Annotated[str, Parameter(description="New date (ISO format)")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_change_date_task(user_id, new_date)
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @patch(
        "/{user_id:uuid}/bio",
        summary="Change bio",
        description="Изменить биографию пользователя",
    )
    async def change_bio(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        new_bio: Annotated[str, Parameter(description="New bio")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_change_bio_task(user_id, new_bio)
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @patch(
        "/{user_id:uuid}/language_code",
        summary="Change language code",
        description="Изменить языковой код пользователя",
    )
    async def change_language_code(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        new_language_code: Annotated[str, Parameter(description="New language code")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_change_language_code_task(user_id, new_language_code)
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @patch(
        "/{user_id:uuid}/avatar_url",
        summary="Change avatar URL",
        description="Изменить URL аватара пользователя",
    )
    async def change_avatar_url(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        new_avatar_url: Annotated[str, Parameter(description="New avatar URL")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_change_avatar_url_task(user_id, new_avatar_url)
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @patch(
        "/{user_id:uuid}/privacy_settings",
        summary="Change privacy settings",
        description="Изменить настройки приватности пользователя",
    )
    async def change_privacy_settings(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        data: PrivacySettingsUpdate,
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            print(f"Privacy settings received: {data.dict()}")
            task_id = await taskiq_service.send_change_privacy_settings_task(
                user_id,
                data.dict()
            )
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @post(
        "/{user_id:uuid}/activate",
        summary="Activate user",
        description="Активировать пользователя",
    )
    async def activate_user(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_activate_user_task(user_id)
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @post(
        "/{user_id:uuid}/deactivate",
        summary="Deactivate user",
        description="Деактивировать пользователя",
    )
    async def deactivate_user(
        self,
        user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_deactivate_user_task(user_id)
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @get(
        "/tasks/{task_id:str}",
        summary="Get task status",
        description="Получить статус асинхронной задачи",
    )
    async def get_task_status(
        self,
        task_id: Annotated[str, Parameter(description="Task ID")],
        taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            result = await taskiq_service.get_task_result(task_id)
            return result
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @patch(
        "/{user_id:uuid}/delete",
        summary="Delete user",
        description="Удалить пользователя",
    )
    async def delete_user(
            self,
            user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
            taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_delete_user_task(user_id)
            return {
                "task_id": task_id,
                "status": "queued",
                "user_id": user_id
            }
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

    @patch(
        "/{user_id:uuid}/block",
        summary="Block user",
        description="Заблокировать пользователя",
    )
    async def block_user(
            self,
            user_id: Annotated[UUID, Parameter(description="User ID (UUID)")],
            taskiq_service: TaskiqService
    ) -> Dict[str, Any]:
        try:
            task_id = await taskiq_service.send_block_user_task(user_id)
            return {
                "task_id": task_id,
                "status": "queued",
                "user_id": user_id
            }
        except Exception as e:
            raise HTTPException(
                detail=str(e),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
