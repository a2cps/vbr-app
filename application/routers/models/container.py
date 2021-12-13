from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["Container"]


class Container(BaseModel):
    container_id: str
    container_tracking_id: Optional[str]
    container_type: str
    location: Optional[str]
    status: Optional[str]
    tracking_id: Optional[str]
