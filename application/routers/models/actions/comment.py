from pydantic import BaseModel, Field
from typing import Optional


class CreateComment(BaseModel):
    comment: str
