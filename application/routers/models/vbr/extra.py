from datetime import date, datetime
from enum import Enum
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Comment(BaseModel):
    event_ts: datetime
    comment: str
