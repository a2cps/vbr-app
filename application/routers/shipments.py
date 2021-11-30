"""VBR Units"""
from vbr.api import VBR_Api
from fastapi import APIRouter, Body, Depends, HTTPException
from ..dependencies import *
from .models import Shipment, CreateShipment
from .builders import build_shipment

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Shipment])
def shipments(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "shipment", limit=common["limit"], offset=common["offset"]
        )
    ]
    shipments = [build_shipment(row, client) for row in rows]
    return shipments


@router.post("/", dependencies=[Depends(role_vbr_write)], response_model=Shipment)
def create_shipment(
    body: CreateShipment = Body(...),
    track_shipment_via_easypost: bool = True,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Create a new Shipment."""
    data = body.dict()
    # TODO Validate proposed tracking ID before is created
    ship_from_local_id = data.pop("ship_from_local_id", None)
    ship_to_local_id = data.pop("ship_to_local_id", None)
    if ship_from_local_id is not None:
        data["ship_from_id"] = client.get_location_by_local_id(
            ship_from_local_id
        ).primary_key_id()
    if ship_to_local_id is not None:
        data["ship_to_id"] = client.get_location_by_local_id(
            ship_to_local_id
        ).primary_key_id()

    # TODO - Should not be hard-coded
    data["project_id"] = 1
    shipment = client.create_shipment(**data)
    # TODO Create a Tracker with EasyPost API
    # Associate listed containers with shipment.
    # TODO: Errors out if a container is already associated with another shipment. Fix in API.
    if isinstance(body.container_local_ids, list):
        for local_id in body.container_local_ids:
            container = client.get_container_by_local_id(local_id)
            client.associate_container_with_shipment(container, shipment)
    return build_shipment(shipment, client)
