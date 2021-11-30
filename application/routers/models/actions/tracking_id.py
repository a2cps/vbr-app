from pydantic import BaseModel, Field
from typing import Optional


class TrackingId(BaseModel):
    tracking_id: str = Field(None, title="New Tracking ID")


class SetTrackingId(TrackingId):
    comment: Optional[str] = Field(None, title="Optional comment")
