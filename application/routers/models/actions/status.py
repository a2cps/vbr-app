from enum import Enum
from typing import Optional

from pydantic import BaseModel


class BiospecimenStatuses(Enum):
    INFLIGHT = "inflight"
    PRESENT = "present"
    SPOILED = "spoiled"
    DEPLETED = "depleted"
    LOST = "lost"
    DESTROYED = "destroyed"
    INUSE = "inuse"
    AVAILABLE = "available"
    CHANGED_VOLUME = "changed_volume"
    THAWED = "thawed"
    FROZEN = "frozen"


class ContainerStatuses(Enum):
    CREATED = "created"
    PRESENT = "present"
    DAMAGED = "damaged"
    MISSING = "missing"
    LOST = "lost"
    DESTROYED = "destroyed"


class RunListStatuses(Enum):
    READY = "ready"
    PROCESSING = "processing"
    PROCESSED = "processed"


class ShipmentStatuses(Enum):
    CREATED = "created"
    SHIPPED = "shipped"
    RECEIVED = "received"
    PROCESSED = "processed"
    DELAYED = "delayed"
    LOST = "lost"


class SetBiospecimenStatus(BaseModel):
    status: BiospecimenStatuses
    comment: Optional[str]


class SetContainerStatus(BaseModel):
    status: ContainerStatuses
    comment: Optional[str]


class SetRunListStatus(BaseModel):
    status: RunListStatuses
    comment: Optional[str]


class SetShipmentStatus(BaseModel):
    status: ShipmentStatuses
    relocate_containers: Optional[bool] = False
    comment: Optional[str]
