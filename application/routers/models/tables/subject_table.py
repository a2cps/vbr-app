from enum import Enum
from typing import List, Literal, Optional

from attrdict import AttrDict
from pydantic import BaseModel, Field
from vbr.api import VBR_Api


class SubjectTable(BaseModel):
    # Open-access fields
    local_id: str
    creation_time: str
    project_name: str
    guid: str


class SubjectTableRestricted(SubjectTable):
    # PHI fields populated from restricted.formname.key
    redcap_record_id: str
    age: Optional[int]
    ethnicity: Optional[str]
    race: Optional[str]
    sex: Optional[str]


def build_subject_table(data: AttrDict, api: VBR_Api) -> SubjectTable:
    # Static values
    resp = {
        "local_id": data.local_id,
        "creation_time": data.creation_time,
        "project_name": data.project.name,
        "guid": data.tracking_id,
    }
    # Computed values
    # None
    return SubjectTable(**resp)


def build_subject_table_restricted(
    data: AttrDict, api: VBR_Api
) -> SubjectTableRestricted:
    resp = build_subject_table(data, api).dict()
    # These are in the original response but are not visible in default view
    resp["redcap_record_id"] = data.source_subject_id
    # Computed values
    resp["age"] = data.restricted.demographics.age
    resp["ethnicity"] = data.restricted.demographics.ethnicity
    resp["race"] = data.restricted.demographics.race
    resp["sex"] = data.restricted.demographics.sex
    return SubjectTableRestricted(**resp)
