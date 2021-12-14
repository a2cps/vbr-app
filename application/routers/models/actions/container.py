from typing import Optional, List

from pydantic import BaseModel

__all__ = ["SetContainer"]


class SetContainer(BaseModel):
    container_id: str
    comment: Optional[str]
