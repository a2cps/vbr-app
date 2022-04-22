from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

__all__ = ["CreateShipment"]


class CreateShipment(BaseModel):
    tracking_id: str
    name: str
    sender_name: Optional[str]
    project_id: str
    ship_from_location_id: str
    ship_to_location_id: str
    container_ids: Optional[List[str]] = Field(default=[])
