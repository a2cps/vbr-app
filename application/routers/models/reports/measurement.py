from typing import List, Optional, Union

from pydantic import BaseModel
from vbr.api import VBR_Api
from vbr.tableclasses.system import VbrRedcapEvent

__all__ = ["MeasurementReport", "build_measurement_report"]


class MeasurementReport(BaseModel):
    local_id: str
    case_guid: str
    creation_time: str
    shipment_tracking_id: Optional[str]
    container_tracking_id: Optional[str]
    biosample_tracking_id: Optional[str]
    tracking_id: Optional[str]
    visit: str
    measurement_type: str
    container_type: str
    status: str


def build_measurement_report(
    measurement_id: int, vbr_api: VBR_Api
) -> MeasurementReport:
    data = {}
    vbr_measurement_type = vbr_api._get_row_from_table_with_id(
        "measurement_type", vbr_measurement.measurement_type
    )
    vbr_container = vbr_api._get_row_from_table_with_id(
        "container", vbr_measurement.container
    )
    vbr_container_type = vbr_api._get_row_from_table_with_id(
        "container_type", vbr_container.container_type
    )
    vbr_shipment = vbr_api.get_shipment_for_container(vbr_container)
    vbr_biosample = vbr_api._get_row_from_table_with_id(
        "biosample", vbr_measurement.biosample
    )
    vbr_protocol = vbr_api._get_row_from_table_with_id(
        "protocol", vbr_biosample.protocol
    )
    vbr_subject = vbr_api._get_row_from_table_with_id("subject", vbr_biosample.subject)

    # Populate values derived from vbr objects
    data["measurement_type"] = getattr(vbr_measurement_type, "name", None)
    data["container_tracking_id"] = getattr(vbr_container, "tracking_id", None)
    data["container_type"] = getattr(vbr_container_type, "name", None)
    data["shipment_tracking_id"] = getattr(vbr_shipment, "tracking_id", None)
    data["case_guid"] = getattr(vbr_subject, "tracking_id", None)
    data["biosample_tracking_id"] = getattr(vbr_biosample, "tracking_id", None)
    data["visit"] = getattr(vbr_protocol, "name", None)

    return MeasurementReport(**data)
