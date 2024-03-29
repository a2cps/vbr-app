from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

__all__ = ["CreateRunList", "CreateRunListWithBiospecimens", "UpdateRunList"]


class CreateRunList(BaseModel):
    runlist_type_id: str
    location_id: str
    name: Optional[str]  = None
    description: Optional[str]  = None
    tracking_id: Optional[str]  = None


class CreateRunListWithBiospecimens(CreateRunList):
    biospecimen_ids: Optional[List[str]] = Field(default=[])


class UpdateRunList(BaseModel):
    location_id: Optional[str]  = None
    name: Optional[str]  = None
    description: Optional[str]  = None
    tracking_id: Optional[str]  = None