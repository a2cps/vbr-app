from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = [
    "Biospecimen",
    "BiospecimenPrivate",
    "BiospecimenPrivateExtended",
]


class Biospecimen(BaseModel):
    biospecimen_id: str
    tracking_id: Optional[str]
    creation_time: Optional[datetime]
    biospecimen_type: str
    collection_id: Optional[str]
    collection_tracking_id: Optional[str]
    container_id: str
    container_tracking_id: Optional[str]
    project: str
    status: str
    unit: str
    subject_guid: UUID
    subject_id: str
    volume: Optional[float]
    bscp_time_blood_draw: Optional[datetime]
    bscp_time_centrifuge: Optional[str]
    bscp_aliquot_freezer_time: Optional[str]
    bscp_deg_of_hemolysis: Optional[float]
    bscp_phleb_by_init: Optional[str]
    bscp_procby_initials: Optional[str]
    bscp_protocol_dev: Optional[bool]
    bscp_comments: Optional[str]
    location_id: Optional[str]
    location_display_name: Optional[str]
    protocol_name: Optional[str]

    class Config:
        orm_mode = True


class BiospecimenPrivate(Biospecimen):
    sex: Optional[str]


class BiospecimenPrivateExtended(BiospecimenPrivate):
    age: Optional[int]
    race: Optional[str]
    ethnicity: Optional[str]
