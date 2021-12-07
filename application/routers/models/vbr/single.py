from enum import Enum
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .primitives import *


class Location(BaseModel):
    _location_id: int
    location_id: str
    display_name: str
    address1: Optional[str]
    address2: Optional[str]
    address3: Optional[str]
    city: Optional[str]
    state_province_country: Optional[str]
    zip_or_postcode: Optional[str]
    organization: Optional[Organization]

    class Config:
        schema_extra = {
            "example": {
                "_location_id": 12345,
                "location_id": "7yKzwW8LXA6vE",
                "display_name": "TACC",
                "address1": "Advanced Computing Building (ACB)",
                "address2": "J.J. Pickle Research Campus, Building 205",
                "address3": "10100 Burnet Rd (R8700)",
                "city": "Austin",
                "state_province_country": "TX",
                "zip_or_postcode": "78758",
                "organization": None,
            }
        }
