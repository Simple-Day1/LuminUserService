from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from LuminUserService.app.domain.models.entities.base_entity import BaseEntity


@dataclass
class ProfileView(BaseEntity):
    view_id: UUID
    viewer_id: UUID
    view_ip: str
    viewed_at: datetime
