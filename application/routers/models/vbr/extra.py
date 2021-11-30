from datetime import date, datetime
from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID


class Comment(BaseModel):
    event_ts: datetime
    comment: str
