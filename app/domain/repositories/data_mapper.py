from abc import ABC, abstractmethod
from LuminUserService.app.domain.models.aggregates.user import User


class UserDataMapper(ABC):
    @abstractmethod
    def to_domain(self, data: dict) -> User:
        pass

    @abstractmethod
    def to_persistence(self, user: User) -> dict:
        pass

    @abstractmethod
    def to_domain_list(self, data_list: list[dict]) -> list[User]:
        pass
