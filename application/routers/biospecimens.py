"""VBR Biospecimen routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api, measurement
from vbr.utils.barcode import generate_barcode_string, sanitize_barcode_string

from application.routers.models.actions import trackingid

from ..dependencies import *
from .models import (
    Biospecimen,
    BiospecimenPrivate,
    BiospecimenPrivateExtended,
    Comment,
    CreateComment,
    Event,
    SetBiospecimenStatus,
    SetContainer,
    SetTrackingId,
    transform,
)

router = APIRouter(
    prefix="/biospecimens",
    tags=["biospecimens"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/", dependencies=[Depends(vbr_read_public)], response_model=List[Biospecimen]
)
def list_biospecimens(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    """List Biospecimens.

    Requires: **VBR_READ_PUBLIC**"""
    # TODO - build up from filters
    query = {}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="biospecimens_details",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/private",
    dependencies=[Depends(vbr_read_limited_phi)],
    response_model=List[BiospecimenPrivate],
)
def list_biospecimens_with_limited_phi(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    """List Biospecimens with limited PHI.

    Requires: **VBR_READ_LIMITED_PHI**"""
    # TODO - build up from filters
    query = {}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="biospecimens_details_private",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{biospecimen_id}",
    dependencies=[Depends(vbr_read_public)],
    response_model=Biospecimen,
)
def get_biospecimen_by_id(
    biospecimen_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Biospecimen by ID.

    Requires: **VBR_READ_PUBLIC**"""
    query = {"biospecimen_id": {"operator": "eq", "value": biospecimen_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.get(
    "/{biospecimen_id}/private",
    dependencies=[Depends(vbr_read_any_phi)],
    response_model=BiospecimenPrivateExtended,
)
def get_biospecimen_by_id_with_extended_phi(
    biospecimen_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Biospecimen with extended PHI by ID.

    Requires: **VBR_READ_ANY_PHI**"""
    query = {"biospecimen_id": {"operator": "eq", "value": biospecimen_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details_private", query=query, limit=1, offset=0
        )[0]
    )
    return row


# GET /tracking/{tracking_id}
@router.get(
    "/tracking/{tracking_id}",
    dependencies=[Depends(vbr_read_public)],
    response_model=Biospecimen,
)
def get_biospecimen_by_id(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Biospecimen by Tracking ID.

    Requires: **VBR_READ_PUBLIC**"""
    tracking_id = sanitize_barcode_string(tracking_id)
    query = {"tracking_id": {"operator": "eq", "value": tracking_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details", query=query, limit=1, offset=0
        )[0]
    )
    return row


# PUT /{biospecimen_id}/container
@router.put(
    "/{biospecimen_id}/container",
    dependencies=[Depends(vbr_write_public)],
    response_model=Biospecimen,
)
def update_biospecimen_container(
    biospecimen_id: str,
    body: SetContainer = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Move a Biospecimen to another Container.

    Requires: **VBR_WRITE_PUBLIC**"""
    biospecimen_id = sanitize_barcode_string(biospecimen_id)
    biospecimen_id = sanitize_barcode_string(body.biospecimen_id)
    measurement = client.rebox_measurement_by_local_id(
        local_id=biospecimen_id, container_local_id=biospecimen_id
    )
    query = {"biospecimen_id": {"operator": "eq", "value": measurement.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details", query=query, limit=1, offset=0
        )[0]
    )
    return row


# PUT /{biospecimen_id}/status
@router.put(
    "/{biospecimen_id}/status",
    dependencies=[Depends(vbr_write_public)],
    response_model=Biospecimen,
)
def update_biospecimen_status(
    biospecimen_id: str,
    body: SetBiospecimenStatus = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update Biospecimen status.

    Requires: **VBR_WRITE_PUBLIC**"""
    biospecimen_id = sanitize_barcode_string(biospecimen_id)
    measurement = client.get_measurement_by_local_id(biospecimen_id)
    measurement = client.update_measurement_status_by_name(
        measurement, status_name=body.status.value, comment=body.comment
    )
    # TODO - take any requisite actions associated with specific statuses
    query = {"biospecimen_id": {"operator": "eq", "value": measurement.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# PUT /{biospecimen_id}/tracking_id
@router.put(
    "/{biospecimen_id}/tracking_id",
    dependencies=[Depends(vbr_read_public)],
    response_model=Biospecimen,
)
def update_biospecimen_tracking_id(
    biospecimen_id: str,
    body: SetTrackingId = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Update a Biospecimen tracking ID.

    Requires: **VBR_WRITE_PUBLIC**"""
    biospecimen_id = sanitize_barcode_string(biospecimen_id)
    tracking_id = sanitize_barcode_string(body.tracking_id)
    # TODO propagate comment
    measurement = client.get_measurement_by_local_id(biospecimen_id)
    measurement.tracking_id = tracking_id
    measurement = client.vbr_client.update_row(measurement)
    query = {"biospecimen_id": {"operator": "eq", "value": measurement.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details", query=query, limit=1, offset=0
        )[0]
    )
    return row


# GET /{biospecimen_id}/events
@router.get(
    "/{biospecimen_id}/events",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[Event],
)
def get_events_for_biospecimen(
    biospecimen_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Events for a Biospecimen.

    Requires: **VBR_READ_PUBLIC**"""
    biospecimen_id = sanitize_barcode_string(biospecimen_id)
    query = {"biospecimen_id": {"operator": "=", "value": biospecimen_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="biospecimens_data_events_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


# GET /{biospecimen_id}/comments
@router.get(
    "/{biospecimen_id}/comments",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[Comment],
)
def get_comments_for_biospecimen(
    biospecimen_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Comments for a Biospecimen.

    Requires: **VBR_READ_PUBLIC**"""
    biospecimen_id = sanitize_barcode_string(biospecimen_id)
    # TODO - change name of field to shipment_tracking_id after updating containers_public.sql
    query = {"biospecimen_id": {"operator": "=", "value": biospecimen_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="biospecimens_comments_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


@router.post(
    "/{biospecimen_id}/comments",
    dependencies=[Depends(vbr_write_public)],
    response_model=Comment,
)
def add_biospecimen_comment(
    biospecimen_id: str,
    body: CreateComment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Add a Comment to a Biospecimen.

    Requires: **VBR_WRITE_PUBLIC**"""
    biospecimen_id = sanitize_barcode_string(biospecimen_id)
    measurement = client.get_measurement_by_local_id(biospecimen_id)
    data_event = client.create_and_link(comment=body.comment, link_target=measurement)[
        0
    ]
    return Comment(comment=data_event.comment, timestamp=data_event.event_ts)


# TODO
# POST /partition - partition a biospecimen into two
