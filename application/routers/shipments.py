"""VBR Shipment routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api, tracking_id
from vbr.utils.barcode import generate_barcode_string, sanitize_identifier_string

from application.routers import container_types
from application.routers.models.actions.comment import Comment
from application.routers.models.actions.shipment import CreateShipment

from ..dependencies import *
from .models import (
    AddContainer,
    Container,
    CreateComment,
    Event,
    SetShipmentStatus,
    Shipment,
    transform,
)
from .utils import parameters_to_query

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
    responses={404: {"description": "Not found"}},
    route_class=LoggingRoute,
)


@router.get("/", dependencies=[Depends(vbr_read_public)], response_model=List[Shipment])
def list_shipments(
    # See views/shipments_public.sql for possible filter names
    shipment_id: Optional[str] = None,
    tracking_id: Optional[str] = None,
    shipment_name: Optional[str] = None,
    sender_name: Optional[str] = None,
    project_name: Optional[str] = None,
    ship_from: Optional[str] = None,
    ship_to: Optional[str] = None,
    status: Optional[str] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List Shipments.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    query = parameters_to_query(
        shipment_id=shipment_id,
        tracking_id=tracking_id,
        shipment_name=shipment_name,
        sender_name=sender_name,
        ship_from=ship_from,
        ship_to=ship_to,
        status=status,
    )
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="shipments_public",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.post("/", dependencies=[Depends(vbr_write_public)], response_model=Shipment)
def create_shipment(
    body: CreateShipment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Create a Shipment.

    Requires: **VBR_WRITE_PUBLIC**"""
    sender_name = body.sender_name
    name = body.name
    tracking_id = sanitize_identifier_string(body.tracking_id)
    project_local_id = sanitize_identifier_string(body.project_id)
    ship_to_local_id = sanitize_identifier_string(body.ship_to_location_id)
    ship_from_local_id = sanitize_identifier_string(body.ship_from_location_id)
    container_ids = [sanitize_identifier_string(c) for c in body.container_ids]

    try:
        project_id = client.get_project_by_local_id(project_local_id).project_id
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Could not find project {0}".format(project_local_id),
        )

    try:
        ship_to_id = client.get_location_by_local_id(ship_to_local_id).location_id
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Could not find location {0}".format(ship_to_local_id),
        )

    try:
        ship_from_id = client.get_location_by_local_id(ship_from_local_id).location_id
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Could not find location {0}".format(ship_from_local_id),
        )

    try:
        containers = [client.get_container_by_local_id(c) for c in container_ids]
    except Exception as exc:
        raise HTTPException(
            status_code=404,
            detail="One or more container_ids could not be resolved: {0}".format(exc),
        )

    data = {
        "name": name,
        "sender_name": sender_name,
        "tracking_id": tracking_id,
        "project_id": project_id,
        "ship_to_id": ship_to_id,
        "ship_from_id": ship_from_id,
    }
    try:
        shipment = client.create_shipment(**data)
        # Ff containers are provided, associate them with Shipment
        for container in containers:
            try:
                client.associate_container_with_shipment(container, shipment)
            except Exception:
                # TODO improve error handling
                raise
        # TODO Create EasyPost tracker
        # Return created shipment
        query = {"shipment_id": {"operator": "eq", "value": shipment.local_id}}
        row = transform(
            client.vbr_client.query_view_rows(
                view_name="shipments_public", query=query, limit=1, offset=0
            )[0]
        )
        return row
    except Exception as exc:
        raise
        # raise HTTPException(status_code=500, detail=str(exc))


@router.get(
    "/{shipment_id}", dependencies=[Depends(vbr_read_public)], response_model=Shipment
)
def get_shipment_by_id(
    shipment_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Shipment by ID.

    Requires: **VBR_READ_PUBLIC**"""
    query = {"shipment_id": {"operator": "eq", "value": shipment_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="shipments_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.get(
    "/tracking/{tracking_id}",
    dependencies=[Depends(vbr_read_public)],
    response_model=Shipment,
)
def get_shipment_by_tracking_id(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Shipment by parcel tracking ID.

    Requires: **VBR_READ_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    query = {"tracking_id": {"operator": "eq", "value": tracking_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="shipments_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# GET /tracking/{tracking_id}/containers
@router.get(
    "/tracking/{tracking_id}/containers",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[Container],
)
def get_containers_in_shipment(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Containers in a Shipment.

    Requires: **VBR_READ_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    # TODO - change name of field to shipment_tracking_id after updating containers_public.sql
    query = {"tracking_id": {"operator": "=", "value": tracking_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="containers_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


# PUT /tracking/{tracking_id}/containers - add a container to a shipment
@router.put(
    "/tracking/{tracking_id}/container",
    dependencies=[Depends(vbr_write_public)],
    response_model=List[Container],
)
def add_container_to_shipment(
    tracking_id: str,
    body: AddContainer = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Add a Container to a Shipment.

    Requires: **VBR_WRITE_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    container_id = sanitize_identifier_string(body.container_id)
    try:
        shipment = client.get_shipment_by_tracking_id(tracking_id)
    except Exception:
        raise HTTPException(
            status_code=404, detail="Shipment {0} not found".format(tracking_id)
        )

    try:
        container = client.get_container_by_local_id(container_id)
    except Exception:
        raise HTTPException(
            status_code=404, detail="Container {0} not found".format(container_id)
        )

    try:
        location = client.get_location(shipment.ship_from)
    except Exception:
        raise HTTPException(
            status_code=404, detail="Location {0} not found".format(shipment.ship_from)
        )

    try:
        client.associate_container_with_shipment(container, shipment)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to associate container with shipment"
        )

    try:
        client.relocate_container(container, location, sync=False)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to update container location"
        )

    # Display updated list of containers associated with shipment
    query = {"tracking_id": {"operator": "=", "value": tracking_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="containers_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


# DELETE /tracking/{tracking_id}/containers/{container_id} - remove a container from a shipment
@router.delete(
    "/tracking/{tracking_id}/container/{container_id}",
    dependencies=[Depends(vbr_write_public)],
    response_model=List[Container],
)
def remove_container_from_shipment(
    tracking_id: str,
    container_id: str,
    client: Tapis = Depends(vbr_admin_client),
):
    """Remove a Container from a Shipment.

    Requires: **VBR_WRITE_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    container_id = sanitize_identifier_string(container_id)
    container = client.get_container_by_local_id(container_id)
    client.disassociate_container_from_shipment(container)

    # Display updated list of containers associated with shipment
    query = {"tracking_id": {"operator": "=", "value": tracking_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="containers_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


# PATCH /tracking/{tracking_id}/status - update status by name
@router.patch(
    "/tracking/{tracking_id}/status",
    dependencies=[Depends(vbr_write_public)],
    response_model=Shipment,
)
def update_shipment_status(
    tracking_id: str,
    body: SetShipmentStatus = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update a Shipment status

    Setting `relocate_containers=true` in the message body
    when event name is `received` will move all containers
    associated with the shipment to the shipment destination.

    Requires: **VBR_WRITE_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    shipment = client.get_shipment_by_tracking_id(tracking_id)
    shipment = client.update_shipment_status_by_name(
        shipment, status_name=body.status.value, comment=body.comment
    )
    # TODO - take any requisite actions associated with specific statuses
    if body.status.value == "received" and body.relocate_containers is True:
        to_location = client.get_location(shipment.ship_to)
        containers = client.get_containers_for_shipment(shipment)
        for container in containers:
            client.relocate_container(container, to_location, sync=False)
    query = {"shipment_id": {"operator": "eq", "value": shipment.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="shipments_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# GET /tracking/{tracking_id}/events
@router.get(
    "/tracking/{tracking_id}/events",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[Event],
)
def get_events_for_shipment(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Events for a Shipment.

    Requires: **VBR_READ_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    # TODO - change name of field to shipment_tracking_id after updating containers_public.sql
    query = {"shipment_tracking_id": {"operator": "=", "value": tracking_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="shipments_data_events_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


# GET /tracking/{tracking_id}/comments
@router.get(
    "/tracking/{tracking_id}/comments",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[Comment],
)
def get_comments_for_shipment(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Comments for a Shipment.

    Requires: **VBR_READ_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    # TODO - change name of field to shipment_tracking_id after updating containers_public.sql
    query = {"shipment_tracking_id": {"operator": "=", "value": tracking_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="shipments_comments_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


@router.post(
    "/tracking/{tracking_id}/comments",
    dependencies=[Depends(vbr_write_public)],
    response_model=Comment,
)
def add_shipment_comment(
    tracking_id: str,
    body: CreateComment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Add a Comment to a Shipment.

    Requires: **VBR_WRITE_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    shipment = client.get_shipment_by_tracking_id(tracking_id)
    data_event = client.create_and_link(comment=body.comment, link_target=shipment)[0]
    return Comment(comment=data_event.comment, timestamp=data_event.event_ts)


# TODO
# POST / - create new shipment
