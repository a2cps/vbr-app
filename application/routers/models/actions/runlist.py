from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

__all__ = ["CreateRunList"]


class CreateRunList(BaseModel):
    name: Optional[str]
    description: Optional[str]
    tracking_id: Optional[str]
    # TODO - consider adding this in
    # biospecimen_ids: Optional[List[str]] = Field(default=[])
