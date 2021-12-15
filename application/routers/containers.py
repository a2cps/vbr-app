"""VBR Container routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api
from vbr.utils.barcode import (generate_barcode_string,
                               sanitize_identifier_string)

from application.routers.models.biospecimen import Biospecimen

from ..dependencies import *
from .models import (Biospecimen, Comment, Container, CreateComment, Event,
                     SetContainerLocation, SetContainerStatus, SetTrackingId,
                     transform)
from .utils import parameters_to_query

router = APIRouter(
    prefix="/containers",
    tags=["containers"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/", dependencies=[Depends(vbr_read_public)], response_model=List[Container]
)
def list_containers(
    # See views/containers_public.sql for possible filter names
    container_id: Optional[str] = None,
    container_tracking_id: Optional[str] = None,
    container_type: Optional[str] = None,
    location: Optional[str] = None,
    status: Optional[str] = None,
    tracking_id: Optional[str] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List Containers.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    query = parameters_to_query(
        container_id=container_id,
        container_tracking_id=container_tracking_id,
        container_type=container_type,
        location=location,
        status=status,
        tracking_id=tracking_id,
    )
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="containers_public",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{container_id}", dependencies=[Depends(vbr_read_public)], response_model=Container
)
def get_container_by_id(
    container_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Container by ID.

    Requires: **VBR_READ_PUBLIC**"""
    query = {"container_id": {"operator": "eq", "value": container_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="containers_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.get(
    "/tracking/{tracking_id}",
    dependencies=[Depends(vbr_read_public)],
    response_model=Container,
)
def get_container_by_tracking_id(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Container by tracking ID.

    Requires: **VBR_READ_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    query = {"container_tracking_id": {"operator": "eq", "value": tracking_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="containers_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# GET /{container_id}/biospecimens
@router.get(
    "/{container_id}/biospecimens",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[Biospecimen],
)
def list_biospecimens_in_container(
    container_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """List Biospecimens in a Container.

    Requires: **VBR_READ_PUBLIC**"""

    container_id = sanitize_identifier_string(container_id)
    query = {"container_id": {"operator": "=", "value": container_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="biospecimens_details",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


# PUT /{container_id}/status - update status by name
@router.put(
    "/{container_id}/status",
    dependencies=[Depends(vbr_write_public)],
    response_model=Container,
)
def update_container_status(
    container_id: str,
    body: SetContainerStatus = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update a Container status.

    Requires: **VBR_WRITE_PUBLIC**"""
    container = client.get_container_by_local_id(container_id)
    container = client.update_container_status_by_name(
        container, status_name=body.status.value, comment=body.comment
    )
    # TODO - take any requisite actions associated with specific statuses
    query = {"container_id": {"operator": "eq", "value": container.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="containers_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.put(
    "/{container_id}/location",
    dependencies=[Depends(vbr_write_public)],
    response_model=Container,
)
def update_container_location(
    container_id: str,
    body: SetContainerLocation = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update a Container's Location.

    Requires: **VBR_WRITE_PUBLIC**"""
    container_id = sanitize_identifier_string(container_id)
    location_id = sanitize_identifier_string(body.location_id)
    container = client.get_container_by_local_id(container_id)
    container = client.relocate_container_by_local_id(
        local_id=container.local_id, location_local_id=location_id
    )
    query = {"container_id": {"operator": "eq", "value": container.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="containers_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.put(
    "/{container_id}/tracking_id",
    dependencies=[Depends(vbr_write_public)],
    response_model=Container,
)
def update_container_tracking_id(
    container_id: str,
    body: SetTrackingId = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update a Container's tracking ID.

    Requires: **VBR_WRITE_PUBLIC**"""
    container_id = sanitize_identifier_string(container_id)
    tracking_id = sanitize_identifier_string(body.tracking_id)
    # TODO propagate comment
    container = client.get_container_by_local_id(container_id)
    container.tracking_id = tracking_id
    container = client.vbr_client.update_row(container)
    query = {"container_id": {"operator": "eq", "value": container.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="containers_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# GET /{container_id}/events
@router.get(
    "/{container_id}/events",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[Event],
)
def get_events_for_container(
    container_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Events for a Container.

    Requires: **VBR_READ_PUBLIC**"""
    container_id = sanitize_identifier_string(container_id)
    # TODO - change name of field to shipment_tracking_id after updating containers_public.sql
    query = {"container_id": {"operator": "=", "value": container_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="containers_data_events_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


# GET /{container_id}/comments
@router.get(
    "/{container_id}/comments",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[Comment],
)
def get_comments_for_container(
    container_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Comments for a Container.

    Requires: **VBR_READ_PUBLIC**"""
    container_id = sanitize_identifier_string(container_id)
    # TODO - change name of field to shipment_tracking_id after updating containers_public.sql
    query = {"container_id": {"operator": "=", "value": container_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="containers_comments_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


@router.post(
    "/{container_id}/comments",
    dependencies=[Depends(vbr_write_public)],
    response_model=Comment,
)
def add_container_comment(
    container_id: str,
    body: CreateComment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Add a Comment to a Container.

    Requires: **VBR_WRITE_PUBLIC**"""
    container_id = sanitize_identifier_string(container_id)
    container = client.get_container_by_local_id(container_id)
    data_event = client.create_and_link(comment=body.comment, link_target=container)[0]
    return Comment(comment=data_event.comment, timestamp=data_event.event_ts)


# TODO
# POST / - create new container
