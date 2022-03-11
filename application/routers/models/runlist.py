from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["RunList"]


class RunList(BaseModel):
    runlist_id: str
    name: str
    description: Optional[str]
    tracking_id: Optional[str]
    status_name: Optional[str]
