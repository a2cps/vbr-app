from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["Biospecimen", "BiospecimenPrivate", "BiospecimenPrivateExtended"]


class Biospecimen(BaseModel):
    biospecimen_id: str
    tracking_id: Optional[str]
    creation_time: datetime
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
    bscp_time_blood_draw: datetime
    bscp_time_centrifuge: datetime
    bscp_aliquot_freezer_time: datetime
    bscp_deg_of_hemolysis: float
    bscp_phleb_by_init: str
    bscp_procby_initials: str
    bscp_protocol_dev: bool
    bscp_comments: str
    location: str


class BiospecimenPrivate(Biospecimen):
    sex: Optional[str]


class BiospecimenPrivateExtended(BiospecimenPrivate):
    age: Optional[int]
    race: Optional[str]
    ethnicity: Optional[str]
