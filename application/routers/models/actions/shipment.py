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

    class Config:
        schema_extra = {
            "example": {
                "tracking_id": "999999999999",
                "name": "Important Shipment",
                "sender_name": "Winship 'Shippy' Shippman",
                "ship_from_location_id": "8rd3VX8PLrjMO",
                "ship_to_location_id": "7ykbk069YDJP",
                "container_ids": ["PRNRNE2wxX5bB", "7RbNKpb3JJ31Y", "8keBME2MOxv72"],
            }
        }
