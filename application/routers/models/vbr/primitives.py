from typing import Optional
from pydantic import BaseModel


class Anatomy(BaseModel):
    anatomy_id: int
    name: Optional[str]
    description: Optional[str]
    id: str


class ContainerType(BaseModel):
    container_type_id: int
    name: str
    description: Optional[str] = None


class MeasurementType(BaseModel):
    measurement_type_id: int
    name: str
    description: Optional[str] = None


class Organization(BaseModel):
    organization_id: int
    name: str
    description: Optional[str] = None
    url: str


class Project(BaseModel):
    project_id: int
    name: str
    description: Optional[str] = None
    abbreviation: Optional[str] = None


class Protocol(BaseModel):
    protocol_id: int
    name: str
    description: Optional[str] = None


class Status(BaseModel):
    status_id: int
    name: str
    description: Optional[str] = None


class Unit(BaseModel):
    unit_id: int
    name: str
    description: Optional[str] = None
