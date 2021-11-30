from typing import List, Optional

from pydantic import BaseModel, Field

from .localid import ContainerLocalId, LocationLocalId, ProjectLocalId


class CreateShipment(BaseModel):
    tracking_id: str = Field(None, title="Shipment Tracking ID")
    name: Optional[str] = Field(None, title="Optional Shipment name")
    sender_name: Optional[str] = Field(None, title="Optional Sender name or initials")
    ship_from_location_id: Optional[LocationLocalId] = Field(
        None, title="Optional Ship From Location Id"
    )
    ship_to_location_id: Optional[LocationLocalId] = Field(
        None, title="Optional Ship To Location Id"
    )
    # project_local_id: Optional[ProjectLocalId]
    container_ids: Optional[List[ContainerLocalId]] = Field(
        None, title="Optional List of Container Ids to add to Shipment"
    )
