from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

__all__ = ["Comment", "CreateComment"]


class Comment(BaseModel):
    timestamp: datetime
    comment: Optional[str]


class CreateComment(BaseModel):
    comment: str

    class Config:
        schema_extra = {
            "example": {
                "comment": "This is a free-text comment",
            }
        }
