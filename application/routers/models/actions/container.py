from typing import List, Optional

from pydantic import BaseModel, Field

__all__ = ["SetContainer", "AddContainer", "CreateContainer"]


class SetContainer(BaseModel):
    container_id: str
    comment: Optional[str]


class AddContainer(BaseModel):
    container_id: str
    comment: Optional[str]


class CreateContainer(BaseModel):
    container_type_id: str
    location_id: Optional[str] = Field(
        None, title="Location. Defaults to 'Default' Location"
    )
    tracking_id: str = "auto"
