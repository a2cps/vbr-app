from typing import Optional

from pydantic import BaseModel, Field


class LocationLocalId(BaseModel):
    location_id: str = Field(None, title="Location Id")


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

    class Config:
        schema_extra = {
            "example": {
                "display_name": "TACC",
                "address1": "Advanced Computing Building (ACB)",
                "address2": "J.J. Pickle Research Campus, Building 205",
                "address3": "10100 Burnet Rd (R8700)",
                "city": "Austin",
                "state_province_country": "TX",
                "zip_or_postcode": "78758",
            }
        }
