from pydantic import BaseModel
from typing import Optional


class SetShipmentMetadata(BaseModel):
    name: Optional[str]
    sender_name: Optional[str]
