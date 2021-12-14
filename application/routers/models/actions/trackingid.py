from typing import Optional

from pydantic import BaseModel, Field

__all__ = ["SetTrackingId"]


class SetTrackingId(BaseModel):
    tracking_id: str = Field(None, title="New Tracking ID")
    comment: Optional[str] = Field(None, title="Optional comment")

    class Config:
        schema_extra = {
            "example": {
                "tracking_id": "newtrackingid",
                "comment": "Optional comment explaining or documenting the change",
            }
        }
