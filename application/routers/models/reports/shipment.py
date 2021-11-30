from typing import List, Optional

from pydantic import BaseModel
from vbr.api import VBR_Api

__all__ = ["ShipmentReport", "build_shipment_report"]


class ShipmentHistory(BaseModel):
    pass


class ShipmentReport(BaseModel):
    local_id: str
    tracking_id: str
    mcc: str
    sender_name: str
    ship_from: str
    ship_to: str
    status: str
    history: List[dict]


def _get_shipment_report_data(shipment_id: int, vbr_api: VBR_Api) -> dict:
    # TODO - in progress
    data = {}
    vbr_shipment = vbr_api._get_row_from_table_with_id("shipment", shipment_id)
    # Static values
    for key in ["local_id", "sender_name", "tracking_id"]:
        data[key] = getattr(vbr_shipment, key, None)

    vbr_project = vbr_api._get_row_from_table_with_id("project", vbr_shipment.project)
    data["mcc"] = getattr(vbr_project, "name", None)

    vbr_shipment_ship_to = vbr_api.get_location(vbr_shipment.ship_to)
    vbr_shipment_ship_from = vbr_api.get_location(vbr_shipment.ship_from)
    data["ship_from"] = getattr(vbr_shipment_ship_from, "display_name", None)
    data["ship_to"] = getattr(vbr_shipment_ship_to, "display_name", None)

    # Status
    vbr_status = vbr_api.get_status(vbr_shipment.status)
    data["status"] = getattr(vbr_status, "name", None)

    # History
    data["history"] = _get_shipment_history_data(vbr_shipment, vbr_api)
    return data


def _get_shipment_history_data(shipment: object, vbr_api: VBR_Api) -> List[dict]:
    events = vbr_api.get_shipment_status_history(shipment)
    history = []
    for e in events:
        history.append(e.dict())
    return history


def build_shipment_report(shipment_id: int, vbr_api: VBR_Api) -> ShipmentReport:
    data = _get_shipment_report_data(shipment_id, vbr_api)
    return ShipmentReport(**data)
