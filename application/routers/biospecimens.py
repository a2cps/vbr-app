"""VBR Biospecimen routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api, measurement
from vbr.utils.barcode import generate_barcode_string, sanitize_identifier_string

from application.routers.models.actions import comment, trackingid

from ..dependencies import *
from .models import (
    Biospecimen,
    BiospecimenPrivate,
    BiospecimenPrivateExtended,
    Comment,
    CreateComment,
    Event,
    GenericResponse,
    PartitionBiospecimen,
    RunListBase,
    SetBiospecimenStatus,
    SetContainer,
    SetTrackingId,
    SetVolume,
    transform,
)
from .utils import parameters_to_query

router = APIRouter(
    prefix="/biospecimens",
    tags=["biospecimens"],
    responses={404: {"description": "Not found"}},
    route_class=LoggingRoute,
)


@router.get(
    "/", dependencies=[Depends(vbr_read_public)], response_model=List[Biospecimen]
)
def list_biospecimens(
    # See views/biospecimens_details.sql for possible filter names
    biospecimen_id: Optional[str] = None,
    tracking_id: Optional[str] = None,
    biospecimen_type: Optional[str] = None,
    collection_id: Optional[str] = None,
    collection_tracking_id: Optional[str] = None,
    container_id: Optional[str] = None,
    container_tracking_id: Optional[str] = None,
    location_id: Optional[str] = None,
    location_display_name: Optional[str] = None,
    protocol_name: Optional[str] = None,
    project: Optional[str] = None,
    status: Optional[str] = None,
    unit: Optional[str] = None,
    subject_id: Optional[str] = None,
    subject_guid: Optional[str] = None,
    bscp_procby_initials: Optional[str] = None,
    bscp_protocol_dev: Optional[bool] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List Biospecimens.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    query = parameters_to_query(
        biospecimen_id=biospecimen_id,
        tracking_id=tracking_id,
        biospecimen_type=biospecimen_type,
        collection_id=collection_id,
        collection_tracking_id=collection_tracking_id,
        container_id=container_id,
        container_tracking_id=container_tracking_id,
        location_id=location_id,
        location_display_name=location_display_name,
        protocol_name=protocol_name,
        project=project,
        status=status,
        unit=unit,
        subject_id=subject_id,
        subject_guid=subject_guid,
        bscp_procby_initials=bscp_procby_initials,
        bscp_protocol_dev=bscp_protocol_dev,
    )
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


# GET /private
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


# GET /{biospecimen_id}
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


# POST /{biospecimen_id}/partition
@router.post(
    "/{biospecimen_id}/partition",
    dependencies=[Depends(vbr_write_public)],
    response_model=Biospecimen,
)
def partition_biospecimen(
    biospecimen_id: str,
    body: PartitionBiospecimen = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Partition a Biospecimen into two Biospecimens.

    Requiress: **VBR_WRITE_PUBLIC**
    """
    biospecimen_id = vbr.utils.sanitize_identifier_string(biospecimen_id)
    new_tracking_id = vbr.utils.sanitize_identifier_string(body.tracking_id)
    measurement = client.get_measurement_by_local_id(biospecimen_id)
    new_measurement = client.partition_measurement(
        measurement, volume=body.volume, tracking_id=new_tracking_id, comment=comment
    )
    query = {"biospecimen_id": {"operator": "eq", "value": new_measurement.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details", query=query, limit=1, offset=0
        )[0]
    )
    return row


# DELETE /{biospecimen_id}
@router.delete(
    "/{biospecimen_id}/partition",
    dependencies=[Depends(vbr_admin)],
    response_model=GenericResponse,
)
def delete_biospecimen(
    biospecimen_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Delete a Biospecimen from the system.

    Requiress: **VBR_ADMIN**
    """
    biospecimen_id = vbr.utils.sanitize_identifier_string(biospecimen_id)
    measurement = client.get_measurement_by_local_id(biospecimen_id)
    client.vbr_client.delete_row(measurement)
    return {"message": "Biospecimen deleted"}


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
    biospecimen_id = vbr.utils.sanitize_identifier_string(biospecimen_id)
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
def get_biospecimen_by_tracking_id(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Biospecimen by Tracking ID.

    Requires: **VBR_READ_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    query = {"tracking_id": {"operator": "eq", "value": tracking_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details", query=query, limit=1, offset=0
        )[0]
    )
    return row


# PATCH /{biospecimen_id}/container
@router.patch(
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
    biospecimen_id = sanitize_identifier_string(biospecimen_id)
    container_id = sanitize_identifier_string(body.container_id)
    measurement = client.rebox_measurement_by_local_id(
        local_id=biospecimen_id, container_local_id=container_id
    )
    query = {"biospecimen_id": {"operator": "eq", "value": measurement.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details", query=query, limit=1, offset=0
        )[0]
    )
    return row


# PATCH /{biospecimen_id}/status
@router.patch(
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
    biospecimen_id = sanitize_identifier_string(biospecimen_id)
    measurement = client.get_measurement_by_local_id(biospecimen_id)
    measurement = client.update_measurement_status_by_name(
        measurement, status_name=body.status.value, comment=body.comment
    )
    # TODO - take any requisite actions associated with specific statuses
    query = {"biospecimen_id": {"operator": "eq", "value": measurement.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details", query=query, limit=1, offset=0
        )[0]
    )
    return row


# PATCH /{biospecimen_id}/tracking_id
@router.patch(
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
    biospecimen_id = sanitize_identifier_string(biospecimen_id)
    tracking_id = sanitize_identifier_string(body.tracking_id)
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


# PATCH /{biospecimen_id}/volume
@router.patch(
    "/{biospecimen_id}/volume",
    dependencies=[Depends(vbr_write_public)],
    response_model=Biospecimen,
)
def update_biospecimen_volume(
    biospecimen_id: str,
    body: SetVolume = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Update a Biospecimen volume.

    Requires: **VBR_WRITE_PUBLIC**"""
    biospecimen_id = sanitize_identifier_string(biospecimen_id)
    volume = body.volume
    comment = body.comment

    measurement = client.get_measurement_by_local_id(biospecimen_id)
    measurement = client.set_volume(measurement, volume, comment)

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
    biospecimen_id = sanitize_identifier_string(biospecimen_id)
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
    biospecimen_id = sanitize_identifier_string(biospecimen_id)
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
    biospecimen_id = sanitize_identifier_string(biospecimen_id)
    measurement = client.get_measurement_by_local_id(biospecimen_id)
    data_event = client.create_and_link(comment=body.comment, link_target=measurement)[
        0
    ]
    return Comment(comment=data_event.comment, timestamp=data_event.event_ts)


# TODO
# POST /partition - partition a biospecimen into two

# GET /{biospecimen_id}/runlists
@router.get(
    "/{biospecimen_id}/runlists",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[RunListBase],
)
def get_runlists_for_biospecimen(
    biospecimen_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Runlists for a Biospecimen.

    Requires: **VBR_READ_PUBLIC**"""
    biospecimen_id = sanitize_identifier_string(biospecimen_id)
    # TODO - change name of field to shipment_tracking_id after updating containers_public.sql
    query = {"biospecimen_id": {"operator": "=", "value": biospecimen_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="runlists_biospecimens_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows
