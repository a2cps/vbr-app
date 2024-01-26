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
    biospecimen_type: str
    collection_id: Optional[str]
    collection_tracking_id: Optional[str]
    container_id: str
    container_tracking_id: Optional[str]
    project: str
    status: str
    unit: str
    subject_id: str
    volume: Optional[float]
    redcap_repeat_instance: Optional[int]
    bscp_deg_of_hemolysis: Optional[float]
    bscp_protocol_dev: Optional[bool]
    bscp_comments: Optional[str]
    collection_site_location_id: Optional[str]
    collection_site_location_display_name: Optional[str]
    location_id: Optional[str]
    location_display_name: Optional[str]
    protocol_name: Optional[str]
    surgery_type: Optional[str]

    class Config:
        orm_mode = True


class BiospecimenPrivate(Biospecimen):
    creation_time: Optional[datetime]
    subject_guid: UUID
    bscp_time_blood_draw: Optional[datetime]
    bscp_time_centrifuge: Optional[str]
    bscp_aliquot_freezer_time: Optional[str]
    bscp_phleb_by_init: Optional[str]
    bscp_procby_initials: Optional[str]
    sex: Optional[str] = None


class BiospecimenPrivateExtended(BiospecimenPrivate):
    age: Optional[int]
    race: Optional[str]
    ethnicity: Optional[str] = None
