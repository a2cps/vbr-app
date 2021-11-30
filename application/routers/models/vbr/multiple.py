from enum import Enum
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID

from .primitives import *
from .single import *


class Container(BaseModel):
    container_id: int
    local_id: str
    tracking_id: str
    container_type: ContainerType
    location: Location
    status: Status


class DataEvent(BaseModel):
    data_event_id: int
    local_id: str
    comment: Optional[str]
    event_ts: Optional[str]
    rank: Optional[int]
    protocol: Optional[Protocol]
    status: Optional[Status]


class Biosample(BaseModel):
    biosample_id: int
    local_id: str
    creation_time: str
    tracking_id: Optional[str]
    protocol: Protocol
    project: Project
    subject: Subject


class Measurement(BaseModel):
    measurement_id: int
    local_id: str
    tracking_id: Optional[str]
    creation_time: str
    biosample: Biosample
    container: Container
    measurement_type: MeasurementType
    project: Project
    status: Status
    unit: Unit


class Shipment(BaseModel):
    shipment_id: int
    local_id: str
    tracking_id: str
    name: Optional[str]
    sender_name: Optional[str]
    project: Project
    ship_from: Optional[Location]
    ship_to: Optional[Location]
    status: Status


class Subject(BaseModel):
    subject_id: int
    local_id: str
    tracking_id: UUID
    creation_time: str
    project: Project
