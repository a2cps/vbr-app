"""VBR Units"""
from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api

from ..dependencies import *
from .builders import build_container, build_shipment
from .models import (
    Comment,
    Container,
    CreateComment,
    SetShipmentMetadata,
    SetShipmentStatus,
    Shipment,
)

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/tracking/{tracking_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Shipment,
)
def shipment_by_tracking_id(
    tracking_id: str, client: VBR_Api = Depends(vbr_admin_client)
):
    ship = client.get_shipment_by_tracking_id(tracking_id)
    return build_shipment(ship, client)


@router.get(
    "/{shipment_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Shipment,
)
def shipment(shipment_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    ship = client.get_shipment_by_local_id(shipment_id)
    return build_shipment(ship, client)


@router.get(
    "/{shipment_id}/containers",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Container],
)
def shipment_containers(shipment_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    ship = client.get_shipment_by_local_id(shipment_id)
    containers = client.get_containers_for_shipment(ship)
    return [build_container(cont, client) for cont in containers]


@router.put(
    "/{shipment_id}/containers",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Container],
)
def add_container_to_shipment(
    shipment_id: str, client: VBR_Api = Depends(vbr_admin_client)
):
    """Add a Container to a Shipment."""
    ship = client.get_shipment_by_local_id(shipment_id)
    containers = client.get_containers_for_shipment(ship)
    return [build_container(cont, client) for cont in containers]


@router.delete(
    "/{shipment_id}/containers/{container_shipment_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Container],
)
def remove_container_from_shipment(
    shipment_id: str,
    container_shipment_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Remove a Container from a Shipment."""
    ship = client.get_shipment_by_local_id(shipment_id)
    containers = client.get_containers_for_shipment(ship)
    return [build_container(cont, client) for cont in containers]


@router.get(
    "/{shipment_id}/comments",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Comment],
)
def shipment_comments(shipment_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """Get Shipment comments"""
    ship = client.get_shipment_by_local_id(shipment_id)
    data_events = client.data_events_for_record(ship)
    return [
        {"event_ts": de.event_ts, "comment": de.comment}
        for de in data_events
        if de.comment is not None
    ]


@router.post(
    "/{shipment_id}/comments",
    dependencies=[Depends(role_vbr_write)],
    response_model=Comment,
)
def add_shipment_comment(
    shipment_id: str,
    body: CreateComment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Add a comment to a Shipment."""
    ship = client.get_shipment_by_local_id(shipment_id)
    data_event = client.create_and_link(comment=body.comment, link_target=ship)[0]
    return Comment(comment=data_event.comment, event_ts=data_event.event_ts)


@router.put(
    "/{shipment_id}/metadata",
    dependencies=[Depends(role_vbr_write)],
    response_model=Shipment,
)
def update_shipment_metadata(
    shipment_id: str,
    body: SetShipmentMetadata = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Update Shipment metadata"""
    vbr_shipment = client.get_shipment_by_local_id(shipment_id)
    body_dict = body.dict()
    for key, value in body_dict.items():
        setattr(vbr_shipment, key, value)
    vbr_shipment = client.vbr_client.update_row(vbr_shipment)
    return build_shipment(vbr_shipment, client)


@router.put(
    "/{shipment_id}/status",
    dependencies=[Depends(role_vbr_write)],
    response_model=Shipment,
)
def update_shipment_status(
    shipment_id: str,
    body: SetShipmentStatus = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update a Shipment's status"""
    ship = client.get_shipment_by_local_id(shipment_id)
    ship = client.update_shipment_status_by_name(
        ship, status_name=body.status.value, comment=body.comment
    )
    # TODO - take any requisite actions associated with specific statuses
    return build_shipment(ship, client)
