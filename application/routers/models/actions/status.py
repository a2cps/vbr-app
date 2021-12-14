from enum import Enum
from typing import Optional

from pydantic import BaseModel


class BiospecimenStatuses(Enum):
    INFLIGHT = "inflight"
    PRESENT = "present"
    SPOILED = "spoiled"
    DEPLETED = "depleted"
    LOST = "lost"


class ContainerStatuses(Enum):
    PRESENT = "present"
    DAMAGED = "damaged"
    MISSING = "missing"
    LOST = "lost"


class ShipmentStatuses(Enum):
    CREATED = "created"
    SHIPPED = "shipped"
    RECEIVED = "received"
    DELAYED = "delayed"
    LOST = "lost"


class SetBiospecimenStatus(BaseModel):
    status: BiospecimenStatuses
    comment: Optional[str]


class SetContainerStatus(BaseModel):
    status: ContainerStatuses
    comment: Optional[str]


class SetShipmentStatus(BaseModel):
    status: ShipmentStatuses
    comment: Optional[str]
