from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID


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
