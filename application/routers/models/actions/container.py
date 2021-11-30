from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional
from ..vbr import Container


class CreateContainerNesting(BaseModel):
    parent_local_id: str
    child_local_id: str
    comment: Optional[str] = Field(None, title="Optional comment")


class ContainerNesting(BaseModel):
    _self: Container
    parent: Container


class CreateContainer(BaseModel):
    # container_type_local_id: str
    location_local_id: Optional[str]
    parent_container_local_id: Optional[str]
    tracking_id: str
