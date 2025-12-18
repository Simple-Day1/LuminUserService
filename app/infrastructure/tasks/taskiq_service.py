from typing import Dict, Any, Optional
from taskiq import TaskiqResult
from uuid import UUID
from LuminUserService.app.infrastructure.tasks.taskiq_broker import get_taskiq_broker
from LuminUserService.app.application.taskiq.user_commands import (
    create_user_task, change_username_task, change_email_task,
    change_phone_task, change_bio_task, activate_user_task,
    deactivate_user_task, block_user_task, record_profile_view_task, get_user_by_id_task, change_date_task,
    change_language_code_task, change_avatar_url_task, change_privacy_settings_task, delete_user_task
)


class TaskiqService:
    def __init__(self) -> None:
        self.broker = get_taskiq_broker()

    @staticmethod
    async def send_get_user_by_id_task(user_id: UUID) -> Optional[Dict]:
        try:
            print(f"[TaskiqService] Sending get_user_by_id_task for {user_id}")

            task = get_user_by_id_task.kiq(str(user_id))
            result: TaskiqResult = await task

            print(f"[TaskiqService] Task sent, task_id: {result.task_id}")

            try:
                task_result = await result.wait_result(timeout=10)
                print("[TaskiqService] Task result received")

                if task_result.is_success:
                    return task_result.return_value
                else:
                    print(f"[TaskiqService] Task failed: {task_result.error}")
                    return None

            except TimeoutError:
                print(f"[TaskiqService] Task timeout for task_id: {result.task_id}")
                return None

        except Exception as e:
            print(f"[TaskiqService] Error in send_get_user_by_id_task: {e}")
            import traceback
            traceback.print_exc()
            return None

    @staticmethod
    async def send_create_user_task(user_data: Dict[str, Any]) -> str:
        task = await create_user_task.kiq(user_data)
        return task.task_id

    @staticmethod
    async def send_change_username_task(user_id: UUID, new_username: Dict[str, str]) -> str:
        task = await change_username_task.kiq(str(user_id), new_username)
        return task.task_id

    @staticmethod
    async def send_change_email_task(user_id: UUID, new_email: str) -> str:
        task = await change_email_task.kiq(str(user_id), new_email)
        return task.task_id

    @staticmethod
    async def send_change_date_task(user_id: UUID, new_date: str) -> str:
        task = await change_date_task.kiq(str(user_id), new_date)
        return task.task_id

    @staticmethod
    async def send_change_phone_task(user_id: UUID, new_phone: str) -> str:
        task = await change_phone_task.kiq(str(user_id), new_phone)
        return task.task_id

    @staticmethod
    async def send_change_bio_task(user_id: UUID, new_bio: str) -> str:
        task = await change_bio_task.kiq(str(user_id), new_bio)
        return task.task_id

    @staticmethod
    async def send_change_language_code_task(user_id: UUID, new_language_code: str) -> str:
        task = await change_language_code_task.kiq(str(user_id), new_language_code)
        return task.task_id

    @staticmethod
    async def send_change_avatar_url_task(user_id: UUID, new_avatar_url: str) -> str:
        task = await change_avatar_url_task.kiq(str(user_id), new_avatar_url)
        return task.task_id

    @staticmethod
    async def send_change_privacy_settings_task(user_id: UUID, new_privacy_settings: dict) -> str:
        print("Start taskiq service send_change_privacy_settings_task method")
        task = await change_privacy_settings_task.kiq(str(user_id), new_privacy_settings)
        return task.task_id

    @staticmethod
    async def send_activate_user_task(user_id: UUID) -> str:
        task = await activate_user_task.kiq(str(user_id))
        return task.task_id

    @staticmethod
    async def send_deactivate_user_task(user_id: UUID) -> str:
        task = await deactivate_user_task.kiq(str(user_id))
        return task.task_id

    @staticmethod
    async def send_block_user_task(user_id: UUID) -> str:
        task = await block_user_task.kiq(str(user_id))
        return task.task_id

    @staticmethod
    async def send_record_profile_view_task(user_id: UUID, viewer_id: UUID, viewer_ip: str) -> str:
        task = await record_profile_view_task.kiq(str(user_id), str(viewer_id), viewer_ip)
        return task.task_id

    async def get_task_result(self, task_id: str) -> Dict[str, Any]:
        try:
            if self.broker:
                result = await self.broker.result_backend.get_result(task_id)
                if result:
                    return {
                        "status": "completed",
                        "result": result.return_value,
                        "error": result.error,
                        "task_id": task_id
                    }

            return {"status": "pending", "task_id": task_id}

        except Exception as e:
            print(f"Error getting task result: {e}")
            return {"status": "error", "task_id": task_id, "error": str(e)}

    @staticmethod
    async def send_delete_user_task(user_id: UUID) -> str:
        task = await delete_user_task.kiq(str(user_id))
        return task.task_id
