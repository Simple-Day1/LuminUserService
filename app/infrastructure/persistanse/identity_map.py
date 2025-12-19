from threading import Lock
from uuid import UUID
from LuminUserService.app.domain.models.aggregates.user import User
from LuminUserService.app.domain.repositories.identity_map import IdentityMap


class UserIdentityMap(IdentityMap):
    def __init__(self) -> None:
        self._map: dict[UUID, User] = {}
        self._lock = Lock()

    def add(self, user: User) -> None:
        with self._lock:
            self._map[user.id] = user

    def get(self, user_id: UUID) -> User | None:
        with self._lock:
            return self._map.get(user_id)

    def remove(self, user_id: UUID) -> None:
        with self._lock:
            del self._map[user_id]

    def clear(self) -> None:
        with self._lock:
            self._map.clear()

    def contains(self, user_id: UUID) -> bool:
        with self._lock:
            return user_id in self._map

    def get_all(self) -> dict[UUID, User]:
        with self._lock:
            return self._map.copy()
