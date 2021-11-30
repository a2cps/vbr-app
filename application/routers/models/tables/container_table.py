from attrdict import AttrDict
from vbr.api import VBR_Api
from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class ContainerTable(BaseModel):
    # Open-access fields
    local_id: str
    tracking_id: str
    container_type_name: str
    location_name: str
    status_name: str
    # TODO list/tree of containers under shipping container


def build_container_table(data: AttrDict, api: VBR_Api) -> ContainerTable:
    # Static values
    resp = {
        "local_id": data.local_id,
        "tracking_id": data.tracking_id,
        "container_type_name": data.container_type.name,
        "location_name": data.location.display_name,
        "status_name": data.status.name,
    }
    # Computed values
    # None
    return ContainerTable(**resp)
