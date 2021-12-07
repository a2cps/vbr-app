from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .primitives import *
from .single import *


class Container(BaseModel):
    _container_id: int
    container_id: str
    tracking_id: str
    container_type: ContainerType
    location: Location
    status: Status

    class Config:
        schema_extra = {
            "example": {
                "_container_id": 12345,
                "container_id": "1y23eBZZ3eVw3",
                "tracking_id": "K_RU_BOX_ALI_12345",
                "container_type": ContainerType.Config.schema_extra["example"],
                "location": Location.Config.schema_extra["example"],
                "status": Status.Config.schema_extra["example"],
            }
        }


class DataEvent(BaseModel):
    _data_event_id: int
    data_event_id: str
    comment: Optional[str]
    event_ts: Optional[str]
    rank: Optional[int]
    protocol: Optional[Protocol]
    status: Optional[Status]


class Subject(BaseModel):
    _subject_id: int
    subject_id: str
    creation_time: str
    tracking_id: UUID
    project: Project

    class Config:
        schema_extra = {
            "example": {
                "_subject_id": 10000,
                "subject_id": "ey2JEJ3nXArvm",
                "creation_time": "2021-12-07T16:06:35.012518Z",
                "tracking_id": "b9ac66c0-9edc-4b63-94fd-ce1b29243064",
                "project": Project.Config.schema_extra["example"],
            }
        }


class Biosample(BaseModel):
    _biosample_id: int
    biosample_id: str
    creation_time: str
    tracking_id: Optional[str]
    protocol: Protocol
    project: Project
    subject: Subject

    class Config:
        schema_extra = {
            "example": {
                "_biosample_id": 12345,
                "biosample_id": "1yEqv8XZL7qEm",
                "creation_time": "2021-04-30",
                "tracking_id": "K_RU_KIT_1234",
                "protocol": Protocol.Config.schema_extra["example"],
                "project": Project.Config.schema_extra["example"],
                "subject": Subject.Config.schema_extra["example"],
            }
        }


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

    class Config:
        schema_extra = {
            "example": {
                "_measurement_id": 12345,
                "measurement_id": "1yEqv8XZL7qEm",
                "creation_time": "2021-04-30T00:00:00Z",
                "tracking_id": "K_RU_P_234",
                "biosample": Biosample.Config.schema_extra["example"],
                "container": Container.Config.schema_extra["example"],
                "measurement_type": MeasurementType.Config.schema_extra["example"],
                "project": Project.Config.schema_extra["example"],
                "status": Status.Config.schema_extra["example"],
                "unit": Unit.Config.schema_extra["example"],
            }
        }


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

    class Config:
        schema_extra = {
            "example": {
                "_shipment_id": 12345,
                "shipment_id": "8kdP2pZKX4p7V",
                "tracking_id": "800162098651",
                "name": "Shipment name",
                "sender_name": "Chuy Tacobot",
                "project": Project.Config.schema_extra["example"],
                "ship_from": Location.Config.schema_extra["example"],
                "ship_to": Location.Config.schema_extra["example"],
                "status": Status.Config.schema_extra["example"],
            }
        }
