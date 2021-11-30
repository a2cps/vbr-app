from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID


class Demographics(BaseModel):
    age: Optional[int]
    ethnicity: Optional[str]
    race: Optional[str]
    sex: Optional[str]
