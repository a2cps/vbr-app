from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = [
    "GenomicsSubjectsPrivate"
]


class GenomicsSubjectsPrivate(BaseModel):
    src_subject_id: str
    interview_date: Optional[str] = None
    interview_age: Optional[int] = None
    sex: Optional[str] = None
    race: Optional[str] = None
    ethnicity: Optional[str] = None
    phenotype: Optional[str] = None
    twins_study: Optional[str] = None
    sibling_study: Optional[str] = None
    family_study: Optional[str] = None
    sample_taken: Optional[str] = None

    class Config:
        orm_mode = True
