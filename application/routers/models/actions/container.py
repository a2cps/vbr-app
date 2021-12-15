from typing import List, Optional

from pydantic import BaseModel

__all__ = ["SetContainer"]


class SetContainer(BaseModel):
    container_id: str
    comment: Optional[str]