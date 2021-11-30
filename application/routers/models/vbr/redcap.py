from enum import Enum
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Demographics(BaseModel):
    age: Optional[int]
    ethnicity: Optional[str]
    race: Optional[str]
    sex: Optional[str]
