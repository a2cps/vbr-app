from enum import Enum
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .primitives import *


class Container(BaseModel):
    _container_id: int
    container_id: str
    tracking_id: str
    location: int
    container_type: ContainerType


class Location(BaseModel):
    _location_id: int
    location_id: str
    display_name: str
    address1: Optional[str]
    address2: Optional[str]
    address3: Optional[str]
    city: Optional[str]
    state_province_country: Optional[str]
    zip_or_postcode: Optional[str]
    organization: Optional[Organization]


class Subject(BaseModel):
    _subject_id: int
    subject_id: str
    creation_time: str
    tracking_id: UUID
    project: Project
