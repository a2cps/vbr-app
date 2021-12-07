from typing import Optional

from pydantic import BaseModel, Field


class CreateComment(BaseModel):
    comment: str

    class Config:
        schema_extra = {
            "example": {
                "comment": "This is a free-text comment",
            }
        }
