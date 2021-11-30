from typing import Optional

from pydantic import BaseModel


class Anatomy(BaseModel):
    _anatomy_id: int
    name: Optional[str]
    description: Optional[str]
    id: str


class ContainerType(BaseModel):
    _container_type_id: int
    name: str
    description: Optional[str] = None


class MeasurementType(BaseModel):
    _measurement_type_id: int
    name: str
    description: Optional[str] = None


class Organization(BaseModel):
    _organization_id: int
    name: str
    description: Optional[str] = None
    url: str


class Project(BaseModel):
    _project_id: int
    name: str
    description: Optional[str] = None
    abbreviation: Optional[str] = None


class Protocol(BaseModel):
    _protocol_id: int
    name: str
    description: Optional[str] = None


class Status(BaseModel):
    _status_id: int
    name: str
    description: Optional[str] = None


class Unit(BaseModel):
    _unit_id: int
    name: str
    description: Optional[str] = None
