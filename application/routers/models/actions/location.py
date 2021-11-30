from pydantic import BaseModel, Field
from typing import Optional


class LocationLocalId(BaseModel):
    local_id: str = Field(None, title="Location Local Id")


class SetLocationLocalId(LocationLocalId):
    comment: Optional[str] = Field(None, title="Optional comment")


class CreateLocation(BaseModel):
    display_name: str
    address1: Optional[str]
    address2: Optional[str]
    address3: Optional[str]
    city: Optional[str]
    state_province_country: Optional[str]
    zip_or_postcode: Optional[str]
