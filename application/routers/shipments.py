"""VBR Shipment routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api, tracking_id
from vbr.utils.barcode import generate_barcode_string, sanitize_barcode_string

from application.routers.models.actions.comment import Comment

from ..dependencies import *
from .models import (Container, CreateComment, Event, SetShipmentStatus,
                     Shipment, transform)

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(vbr_read_public)], response_model=List[Shipment])
def list_shipments(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    """List Shipments.

    Requires: **VBR_READ_PUBLIC**"""
    # TODO - build up from filters
    query = {}
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
    tracking_id = sanitize_barcode_string(tracking_id)
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
    tracking_id = sanitize_barcode_string(tracking_id)
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


# PUT /tracking/{tracking_id}/status - update status by name
@router.put(
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

    Requires: **VBR_WRITE_PUBLIC**"""
    tracking_id = sanitize_barcode_string(tracking_id)
    shipment = client.get_shipment_by_tracking_id(tracking_id)
    shipment = client.update_shipment_status_by_name(
        shipment, status_name=body.status.value, comment=body.comment
    )
    # TODO - take any requisite actions associated with specific statuses
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
    tracking_id = sanitize_barcode_string(tracking_id)
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
    tracking_id = sanitize_barcode_string(tracking_id)
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
    tracking_id = sanitize_barcode_string(tracking_id)
    shipment = client.get_shipment_by_tracking_id(tracking_id)
    data_event = client.create_and_link(comment=body.comment, link_target=shipment)[0]
    return Comment(comment=data_event.comment, timestamp=data_event.event_ts)


# TODO
# POST / - create new shipment
