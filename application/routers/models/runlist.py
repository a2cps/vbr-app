from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["BiospecimenIds", "RunList", "RunListBase"]


class BiospecimenIds(BaseModel):
    biospecimen_id: str
    biospecimen_tracking_id: Optional[str] = None


class RunListBase(BaseModel):
    runlist_id: str
    name: str
    description: Optional[str] = None
    location_id: str


class RunList(RunListBase):
    status_name: Optional[str] = None
    tracking_id: Optional[str] = None
    type: Optional[str]
    location_display_name: Optional[str] = None
