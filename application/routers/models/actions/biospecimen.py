from lib2to3.pytree import Base
from typing import List, Optional

from pydantic import BaseModel, Field

__all__ = ["AddBiospecimen", "PartitionBiospecimen", "SetVolume"]


class AddBiospecimen(BaseModel):
    biospecimen_id: str
    comment: Optional[str]


class PartitionBiospecimen(BaseModel):
    volume: float
    tracking_id: Optional[str] = Field(
        None, title="Optional tracking ID for new Measurement"
    )
    comment: Optional[str] = Field(None, title="Optional comment")


class SetVolume(BaseModel):
    volume: float
    comment: Optional[str] = Field(None, title="Optional comment")
