from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["Event"]

# views/data_events_base.sql
class Event(BaseModel):
    data_event_id: str
    timestamp: datetime
    comment: Optional[str]
    status_name: Optional[str]
    status_description: Optional[str]
    protocol_name: Optional[str]
    protocol_description: Optional[str]
