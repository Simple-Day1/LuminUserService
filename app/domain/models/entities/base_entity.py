import uuid
from abc import ABC


class BaseEntity(ABC):
    def __init__(self, entity_id: uuid) -> None:
        self._id: uuid = entity_id or self._generate_entity_id()

    @staticmethod
    def _generate_entity_id() -> uuid:
        return uuid.uuid4().hex

    @property
    def id(self) -> uuid:
        return self._id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash((self.id, type(self).__name__))
