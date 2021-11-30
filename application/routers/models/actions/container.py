from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from ..vbr import Container


class CreateContainerNesting(BaseModel):
    parent_container_id: str
    child_container_id: str
    comment: Optional[str] = Field(None, title="Optional comment")


class ContainerNesting(BaseModel):
    _self: Container
    parent: Container


class CreateContainer(BaseModel):
    # container_type_local_id: str
    location_id: Optional[str]
    parent_container_id: Optional[str]
    tracking_id: str
