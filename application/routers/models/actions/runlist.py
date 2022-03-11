from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

__all__ = ["CreateRunList"]


class CreateRunList(BaseModel):
    name: str
    description: Optional[str]
    sender_name: Optional[str]
    tracking_id: Optional[str]
    biospecimen_ids: Optional[List[str]] = Field(default=[])
