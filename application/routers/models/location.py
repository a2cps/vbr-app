from enum import Enum
from typing import Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field

__all__ = ["Location"]


class Location(BaseModel):
    location_id: str
    display_name: str
    address1: Optional[str]
    address2: Optional[str]
    address3: Optional[str]
    city: Optional[str]
    state_province_country: Optional[str]
    zip_or_postcode: Optional[str]
    organization: Optional[str]
