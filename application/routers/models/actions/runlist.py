from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

__all__ = ["CreateRunList", "CreateRunListWithBiospecimens", "UpdateRunList"]


class CreateRunList(BaseModel):
    runlist_type_id: str
    location_id: str
    name: Optional[str]
    description: Optional[str]
    tracking_id: Optional[str]


class CreateRunListWithBiospecimens(CreateRunList):
    biospecimen_ids: Optional[List[str]] = Field(default=[])


class UpdateRunList(BaseModel):
    location_id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    tracking_id: Optional[str]
