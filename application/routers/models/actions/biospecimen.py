from typing import List, Optional

from pydantic import BaseModel, Field

__all__ = ["PartitionBiospecimen"]


class PartitionBiospecimen(BaseModel):
    tracking_id: Optional[str] = Field(
        None, title="Optional tracking ID for new Measurement"
    )
    comment: Optional[str] = Field(None, title="Optional comment")
