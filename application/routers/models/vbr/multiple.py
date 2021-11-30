from enum import Enum
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID

from .primitives import *
from .single import *


class Container(BaseModel):
    _container_id: int
    container_id: str
    tracking_id: str
    container_type: ContainerType
    location: Location
    status: Status


class DataEvent(BaseModel):
    _data_event_id: int
    data_event_id: str
    comment: Optional[str]
    event_ts: Optional[str]
    rank: Optional[int]
    protocol: Optional[Protocol]
    status: Optional[Status]


class Biosample(BaseModel):
    _biosample_id: int
    biosample_id: str
    creation_time: str
    tracking_id: Optional[str]
    protocol: Protocol
    project: Project
    subject: Subject


class Measurement(BaseModel):
    _measurement_id: int
    measurement_id: str
    tracking_id: Optional[str]
    creation_time: str
    biosample: Biosample
    container: Container
    measurement_type: MeasurementType
    project: Project
    status: Status
    unit: Unit


class Shipment(BaseModel):
    _shipment_id: int
    shipment_id: str
    tracking_id: str
    name: Optional[str]
    sender_name: Optional[str]
    project: Project
    ship_from: Optional[Location]
    ship_to: Optional[Location]
    status: Status


class Subject(BaseModel):
    _subject_id: int
    subject_id: str
    tracking_id: UUID
    creation_time: str
    project: Project
