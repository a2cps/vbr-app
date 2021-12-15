from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["Unit"]


class Unit(BaseModel):
    unit_id: str
    name: str
    description: Optional[str]
