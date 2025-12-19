from abc import ABC, abstractmethod
from typing import Callable, Type
from LuminUserService.app.domain.events.domain_event import DomainEvent
from LuminUserService.app.domain.models.aggregates.aggregate_root import AggregateRoot


class EventBus(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        pass

    @abstractmethod
    def subscribe(self, event_type: Type[DomainEvent], handler: Callable) -> None:
        pass

    @abstractmethod
    async def process_events(self, aggregate: AggregateRoot) -> None:
        pass
