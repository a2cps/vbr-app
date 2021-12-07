from datetime import date, datetime
from enum import Enum
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Comment(BaseModel):
    event_ts: datetime
    comment: str

    class Config:
        schema_extra = {
            "example": {
                "event_ts": "2021-12-07T16:06:35.012518Z",
                "comment": "This is a free-text comment",
            }
        }
