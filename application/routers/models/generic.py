from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["GenericResponse"]


class GenericResponse(BaseModel):
    message: str
    details: Optional[str]
