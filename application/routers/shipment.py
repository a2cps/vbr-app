"""VBR Units"""
from vbr.api import VBR_Api
from fastapi import APIRouter, Body, Depends, HTTPException
from ..dependencies import *
from .models import (
    Container,
    Comment,
    CreateComment,
    Shipment,
    SetShipmentMetadata,
    SetShipmentStatus,
)
from .builders import build_container, build_shipment

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{tracking_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Shipment,
)
def shipment_by_tracking_id(
    tracking_id: str, client: VBR_Api = Depends(vbr_admin_client)
):
    ship = client.get_shipment_by_tracking_id(tracking_id)
    return build_shipment(ship, client)


@router.get(
    "/{local_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Shipment,
)
def shipment(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    ship = client.get_shipment_by_local_id(local_id)
    return build_shipment(ship, client)


@router.get(
    "/{local_id}/containers",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Container],
)
def shipment_containers(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    ship = client.get_shipment_by_local_id(local_id)
    containers = client.get_containers_for_shipment(ship)
    return [build_container(cont, client) for cont in containers]


@router.put(
    "/{local_id}/containers",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Container],
)
def add_container_to_shipment(
    local_id: str, client: VBR_Api = Depends(vbr_admin_client)
):
    """Add a Container to a Shipment."""
    ship = client.get_shipment_by_local_id(local_id)
    containers = client.get_containers_for_shipment(ship)
    return [build_container(cont, client) for cont in containers]


@router.delete(
    "/{local_id}/containers/{container_local_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Container],
)
def remove_container_from_shipment(
    local_id: str, container_local_id: str, client: VBR_Api = Depends(vbr_admin_client)
):
    """Remove a Container from a Shipment."""
    ship = client.get_shipment_by_local_id(local_id)
    containers = client.get_containers_for_shipment(ship)
    return [build_container(cont, client) for cont in containers]


@router.get(
    "/{local_id}/comments",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Comment],
)
def shipment_comments(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """Get Shipment comments"""
    ship = client.get_shipment_by_local_id(local_id)
    data_events = client.data_events_for_record(ship)
    return [
        {"event_ts": de.event_ts, "comment": de.comment}
        for de in data_events
        if de.comment is not None
    ]


@router.post(
    "/{local_id}/comments",
    dependencies=[Depends(role_vbr_write)],
    response_model=Comment,
)
def add_shipment_comment(
    local_id: str,
    body: CreateComment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Add a comment to a Shipment."""
    ship = client.get_shipment_by_local_id(local_id)
    data_event = client.create_and_link(comment=body.comment, link_target=ship)[0]
    return Comment(comment=data_event.comment, event_ts=data_event.event_ts)


@router.put(
    "/{local_id}/metadata",
    dependencies=[Depends(role_vbr_write)],
    response_model=Shipment,
)
def update_shipment_metadata(
    local_id: str,
    body: SetShipmentMetadata = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Update Shipment metadata"""
    vbr_shipment = client.get_shipment_by_local_id(local_id)
    body_dict = body.dict()
    for key, value in body_dict.items():
        setattr(vbr_shipment, key, value)
    vbr_shipment = client.vbr_client.update_row(vbr_shipment)
    return build_shipment(vbr_shipment, client)


@router.put(
    "/{local_id}/status",
    dependencies=[Depends(role_vbr_write)],
    response_model=Shipment,
)
def update_shipment_status(
    local_id: str,
    body: SetShipmentStatus = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update a Shipment's status"""
    ship = client.get_shipment_by_local_id(local_id)
    ship = client.update_shipment_status_by_name(
        ship, status_name=body.status.value, comment=body.comment
    )
    # TODO - take any requisite actions associated with specific statuses
    return build_shipment(ship, client)
