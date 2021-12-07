from typing import Optional

from pydantic import BaseModel


class SetShipmentMetadata(BaseModel):
    name: Optional[str]
    sender_name: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Important Shipment",
                "sender_name": "Winship 'Shippy' Shippman",
            }
        }
