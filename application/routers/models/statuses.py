from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ContainerStatus(BaseModel):
    status: str


class ContainerStatuses(Enum):
    SHIPMENT_SHIPPED = "CONTAINER_PRESENT"
    SHIPMENT_RECEIVED = "CONTAINER_DAMAGED"
    SHIPMENT_DELAYED = "CONTAINER_MISSING"
    SHIPMENT_LOST = "CONTAINER_LOST"


class ContainerStatus(BaseModel):
    status: ContainerStatuses
    comment: Optional[str]


class ShipmentStatus(BaseModel):
    status: str


class ShipmentStatuses(Enum):
    SHIPMENT_SHIPPED = "SHIPMENT_SHIPPED"
    SHIPMENT_RECEIVED = "SHIPMENT_RECEIVED"
    SHIPMENT_DELAYED = "SHIPMENT_DELAYED"
    SHIPMENT_LOST = "SHIPMENT_LOST"


class SetShipmentStatus(BaseModel):
    status: ShipmentStatuses
    comment: Optional[str]
