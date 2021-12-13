from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["Subject", "SubjectPrivate", "SubjectPrivateExtended"]


class Subject(BaseModel):
    """Baseline Subject class"""

    _subject_id: int
    subject_guid: UUID
    subject_id: str
    project: str


class SubjectPrivate(Subject):
    """Subject including biological sex at birth"""

    sex: Optional[str]


class SubjectPrivateExtended(SubjectPrivate):
    """Subject including biological sex and demographics"""

    age: Optional[int]
    race: Optional[str]
    ethnicity: Optional[str]
