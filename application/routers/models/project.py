from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["Project"]


class Project(BaseModel):
    project_id: str
    # creation_time: datetime
    abbreviation: str
    name: str
    description: Optional[str]
