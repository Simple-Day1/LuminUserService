from abc import ABC, abstractmethod
from uuid import UUID
from LuminUserService.app.domain.models.aggregates.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        pass
