from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["Organization"]


class Organization(BaseModel):
    organization_id: str
    name: str
    description: Optional[str]
    url: Optional[str]
