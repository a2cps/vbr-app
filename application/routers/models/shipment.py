from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["Shipment"]


class Shipment(BaseModel):
    shipment_id: str
    tracking_id: str
    shipment_name: Optional[str]
    sender_name: Optional[str]
    project_name: str
    ship_from: str
    ship_to: str
    status: str
