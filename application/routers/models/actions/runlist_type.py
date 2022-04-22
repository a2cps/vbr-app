from typing import List, Optional

from pydantic import BaseModel, Field

__all__ = ["CreateRunlistType"]


class CreateRunlistType(BaseModel):
    name: str
    description: Optional[str]
