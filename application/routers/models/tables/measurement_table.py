from attrdict import AttrDict
from vbr.api import VBR_Api
from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class MeasurementTable(BaseModel):
    local_id: str
    tracking_id: str
    creation_time: str
    biosample_tracking_id: str
    protocol_name: str
    project_name: str
    subject_tracking_id: str
    container_tracking_id: str
    container_location_display_name: str
    measurement_type_name: str
    status_name: str
    unit_name: str
    shipment_tracking_id: str


def build_measurement_table(data: AttrDict, api: VBR_Api) -> MeasurementTable:
    # Static values
    resp = {
        "local_id": data.local_id,
        "tracking_id": data.tracking_id,
        "creation_time": data.creation_time,
        "biosample_tracking_id": data.biosample.tracking_id,
        "protocol_name": data.biosample.protocol.name,
        "project_name": data.project.name,
        "subject_tracking_id": data.biosample.subject.tracking_id,
        "container_tracking_id": data.container.tracking_id,
        "container_location_display_name": data.container.location.display_name,
        "measurement_type_name": data.measurement_type.name,
        "status_name": data.status.name,
        "unit_name": data.unit.name,
        "container_location_name": data.container.location.display_name,
    }
    # Computed values
    # MOCK FOR NOW
    # Use API method for walking up container hiearchy until
    # a shipping box + shipment is found
    resp["shipment_tracking_id"] = "0xDEADBEEF"
    return MeasurementTable(**resp)
