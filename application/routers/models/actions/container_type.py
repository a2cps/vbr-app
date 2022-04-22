from typing import List, Optional

from pydantic import BaseModel, Field

__all__ = ["CreateContainerType"]


class CreateContainerType(BaseModel):
    name: str
    description: Optional[str]
