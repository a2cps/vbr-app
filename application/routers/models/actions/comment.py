from typing import Optional

from pydantic import BaseModel, Field


class CreateComment(BaseModel):
    comment: str
