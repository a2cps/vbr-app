from typing import Optional

from pydantic import BaseModel


class SetShipmentMetadata(BaseModel):
    name: Optional[str]
    sender_name: Optional[str]
