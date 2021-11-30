from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID

from .primitives import *


class Container(BaseModel):
    container_id: int
    local_id: str
    tracking_id: str
    location: int
    container_type: ContainerType


class Location(BaseModel):
    location_id: int
    local_id: str
    display_name: str
    address1: Optional[str]
    address2: Optional[str]
    address3: Optional[str]
    city: Optional[str]
    state_province_country: Optional[str]
    zip_or_postcode: Optional[str]
    organization: Optional[Organization]


class Subject(BaseModel):
    subject_id: int
    local_id: str
    creation_time: str
    tracking_id: UUID
    project: Project
