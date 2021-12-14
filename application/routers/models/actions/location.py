from typing import Optional

from pydantic import BaseModel

__all__ = ["SetContainerLocation"]


class SetContainerLocation(BaseModel):
    location_id: str
    comment: Optional[str]
