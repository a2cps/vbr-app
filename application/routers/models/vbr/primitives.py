from typing import Optional

from pydantic import BaseModel


class Anatomy(BaseModel):
    _anatomy_id: int
    anatomy_id: str
    name: Optional[str]
    description: Optional[str]
    id: str


class ContainerType(BaseModel):
    _container_type_id: int
    container_type_id: str
    name: str
    description: Optional[str] = None


class MeasurementType(BaseModel):
    _measurement_type_id: int
    measurement_type_id: str
    name: str
    description: Optional[str] = None


class Organization(BaseModel):
    _organization_id: int
    organization_id: str
    name: str
    description: Optional[str] = None
    url: str


class Project(BaseModel):
    _project_id: int
    project_id: str
    name: str
    description: Optional[str] = None
    abbreviation: Optional[str] = None


class Protocol(BaseModel):
    _protocol_id: int
    protocol_id: str
    name: str
    description: Optional[str] = None


class Status(BaseModel):
    _status_id: int
    status_id: str
    name: str
    description: Optional[str] = None


class Unit(BaseModel):
    _unit_id: int
    unit_id: str
    name: str
    description: Optional[str] = None
