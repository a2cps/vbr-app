from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ContainerStatuses(Enum):
    PRESENT = "present"
    DAMAGED = "damaged"
    MISSING = "missing"
    LOST = "lost"


class MeasurementStatuses(Enum):
    INFLIGHT = "inflight"
    PRESENT = "present"
    SPOILED = "spoiled"
    DEPLETED = "depleted"
    LOST = "lost"


class ShipmentStatuses(Enum):
    CREATED = "created"
    SHIPPED = "shipped"
    RECEIVED = "received"
    DELAYED = "delayed"
    LOST = "lost"


class SetContainerStatus(BaseModel):
    status: ContainerStatuses
    comment: Optional[str]


class SetMeasurementStatus(BaseModel):
    status: MeasurementStatuses
    comment: Optional[str]


class SetShipmentStatus(BaseModel):
    status: ShipmentStatuses
    comment: Optional[str]
