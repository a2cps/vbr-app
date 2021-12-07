from typing import Optional

from pydantic import BaseModel


class Anatomy(BaseModel):
    _anatomy_id: int
    anatomy_id: str
    name: Optional[str]
    description: Optional[str]
    id: str

    class Config:
        schema_extra = {
            "example": {
                "_anatomy_id": 12345,
                "anatomy_id": "erqygK0PwR96g",
                "name": "blood",
                "description": "whole blood",
                "id": "UBERON:0000178",
            }
        }


class ContainerType(BaseModel):
    _container_type_id: int
    container_type_id: str
    name: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "_container_type_id": 12345,
                "container_type_id": "7qr3MgE286emA",
                "name": "blood aliquot freezer box",
                "description": "",
            }
        }


class MeasurementType(BaseModel):
    _measurement_type_id: int
    measurement_type_id: str
    name: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "_measurement_type_id": 12345,
                "measurement_type_id": "10ebKoX0m4kkZ",
                "name": "generic liquid sample",
                "description": "",
            }
        }


class Organization(BaseModel):
    _organization_id: int
    organization_id: str
    name: str
    description: Optional[str] = None
    url: str

    class Config:
        schema_extra = {
            "example": {
                "_organization_id": 12345,
                "organization_id": "7qrjDr0rEb4RY",
                "name": "UIOWA",
                "description": "University of Iowa",
                "url": "uiowa.edu",
            }
        }


class Project(BaseModel):
    _project_id: int
    project_id: str
    name: str
    description: Optional[str] = None
    abbreviation: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "_project_id": 12345,
                "project_id": "10eb6nrKe9YWn",
                "name": "A2CPS Main",
                "description": "Acute to Chronic Pain Signatures Project",
                "creation_time": "2020-09-01T00:00:00",
                "abbreviation": "A2CPS",
            }
        }


class Protocol(BaseModel):
    _protocol_id: int
    protocol_id: str
    name: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "_protocol_id": 12345,
                "protocol_id": "erqPw5ozN4y82",
                "name": "baseline_visit",
                "description": "Baseline visit",
            }
        }


class Status(BaseModel):
    _status_id: int
    status_id: str
    name: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "_status_id": 12345,
                "status_id": "10ebD5AyveK38",
                "name": "created",
                "description": "Created in VBR",
            }
        }


class Unit(BaseModel):
    _unit_id: int
    unit_id: str
    name: str
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "_unit_id": 12345,
                "unit_id": "Pxw2we8Y1xpze",
                "name": "plasma_aliquot_tube",
                "description": "",
            }
        }
