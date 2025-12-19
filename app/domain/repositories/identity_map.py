from abc import ABC, abstractmethod
from uuid import UUID
from LuminUserService.app.domain.models.aggregates.user import User


class IdentityMap(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    def remove(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def contains(self, user_id: UUID) -> bool:
        pass
