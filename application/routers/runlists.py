"""VBR RunListroutes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from pyparsing import col
from vbr.api import VBR_Api, tracking_id
from vbr.utils.barcode import generate_barcode_string, sanitize_identifier_string

# from application.routers import container_types
from application.routers.models.actions.comment import Comment
from application.routers.models.actions.runlist import CreateRunList

from ..dependencies import *
from .models import (
    AddBiospecimen,
    BiospecimenIds,
    CreateComment,
    Event,
    SetRunListStatus,
    RunList,
    transform,
)
from .utils import parameters_to_query

router = APIRouter(
    prefix="/runlists",
    tags=["runlists"],
    responses={404: {"description": "Not found"}},
    route_class=LoggingRoute,
)

# GET /runlists
@router.get("/", dependencies=[Depends(vbr_read_public)], response_model=List[RunList])
def list_runlists(
    # See views/runlists_base.sql for possible filter names
    runlist_id: Optional[str] = None,
    tracking_id: Optional[str] = None,
    name: Optional[str] = None,
    status_name: Optional[str] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List RunLists.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    query = parameters_to_query(
        runlist_id=runlist_id,
        tracking_id=tracking_id,
        name=name,
        status_name=status_name,
    )
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="runlists_base",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


# POST /runlists
# Create a runlist
@router.post("/", dependencies=[Depends(vbr_write_public)], response_model=RunList)
def create_runlist(
    body: CreateRunList = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Create a RunList.

    Requires: **VBR_WRITE_PUBLIC**"""
    sender_name = body.sender_name
    name = body.name
    tracking_id = sanitize_identifier_string(body.tracking_id)
    project_local_id = sanitize_identifier_string(body.project_id)
    ship_to_local_id = sanitize_identifier_string(body.ship_to_location_id)
    ship_from_local_id = sanitize_identifier_string(body.ship_from_location_id)
    container_ids = [sanitize_identifier_string(c) for c in body.container_ids]
    project_id = client.get_project_by_local_id(project_local_id).project_id
    ship_to_id = client.get_location_by_local_id(ship_to_local_id).location_id
    ship_from_id = client.get_location_by_local_id(ship_from_local_id).location_id
    try:
        containers = [client.get_container_by_local_id(c) for c in container_ids]
    except Exception as exc:
        raise HTTPException(
            status_code=500,
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


# GET /runlists/:id:
# Get runlist by its identifier
@router.get(
    "/{runlist_id}", dependencies=[Depends(vbr_read_public)], response_model=RunList
)
def get_runlist_by_id(
    runlist_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a RunList by ID.

    Requires: **VBR_READ_PUBLIC**"""
    try:
        query = {"runlist_id": {"operator": "eq", "value": runlist_id}}
        row = transform(
            client.vbr_client.query_view_rows(
                view_name="runlists_base", query=query, limit=1, offset=0
            )[0]
        )
        return row
    except IndexError:
        raise HTTPException(status_code=404)
    except Exception:
        raise


# GET /runlists/tracking/:id:
# Get runlist by its tracking identifier
@router.get(
    "/tracking/{tracking_id}",
    dependencies=[Depends(vbr_read_public)],
    response_model=RunList,
)
def get_runlist_by_tracking_id(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a RunList by tracking ID.

    Requires: **VBR_READ_PUBLIC**"""
    tracking_id = sanitize_identifier_string(tracking_id)
    query = {"tracking_id": {"operator": "eq", "value": tracking_id}}
    try:
        row = transform(
            client.vbr_client.query_view_rows(
                view_name="runlists_base", query=query, limit=1, offset=0
            )[0]
        )
        return row
    except IndexError:
        raise HTTPException(status_code=404)
    except Exception:
        raise


# GET /:id:/biospecimens
# List biospecimens in RunList
@router.get(
    "/{runlist_id}/biospecimens",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[BiospecimenIds],
)
def get_biospeciments_in_runlist(
    runlist_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Biospecimens in a RunList.

    Requires: **VBR_READ_PUBLIC**
    """
    query = {"runlist_id": {"operator": "=", "value": runlist_id}}
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


# PUT /:id:/biospecimens
# Ddd a biospecimen to a runlist
@router.put(
    "/{runlist_id}/biospecimens",
    dependencies=[Depends(vbr_write_public)],
    response_model=List[BiospecimenIds],
)
def add_biospecimen_to_runlist(
    runlist_id: str,
    body: AddBiospecimen = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Add a Biospecimen to a RunList.

    Requires: **VBR_WRITE_PUBLIC**
    """
    runlist_id = sanitize_identifier_string(runlist_id)
    biospecimen_id = sanitize_identifier_string(body.biospecimen_id)

    # A runlist is just a VBR schema collection
    collection = client.get_collection_by_local_id(runlist_id)
    # A biospecimen is a VBR schema 'measurement'
    measurement = client.get_measurement_by_local_id(biospecimen_id)

    client.associate_measurement_with_collection(measurement, collection)

    query = {"runlist_id": {"operator": "=", "value": runlist_id}}
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


# DELETE /{runlist_id}/biospecimens/{biospecimen_id}
# Remove a biospecimen from a runlist
@router.delete(
    "/{runlist_id}/biospecimens/{biospecimen_id}",
    dependencies=[Depends(vbr_write_public)],
    response_model=List[BiospecimenIds],
)
def remove_biospecimen_from_runlist(
    runlist_id: str,
    biospecimen_id: str,
    client: Tapis = Depends(vbr_admin_client),
):
    """Remove a Biospecimen from a RunList.

    Requires: **VBR_WRITE_PUBLIC**"""
    runlist_id = sanitize_identifier_string(runlist_id)
    biospecimen_id = sanitize_identifier_string(biospecimen_id)
    # A runlist is just a VBR schema collection
    collection = client.get_collection_by_local_id(runlist_id)
    # A biospecimen is a VBR schema 'measurement'
    measurement = client.get_measurement_by_local_id(biospecimen_id)

    client.disassociate_measurement_from_collection(measurement, collection)

    query = {"runlist_id": {"operator": "=", "value": runlist_id}}
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


# PATCH /{runlist_id}/status
# Update status by name
@router.patch(
    "/{runlist_id}/status",
    dependencies=[Depends(vbr_write_public)],
    response_model=RunList,
)
def update_runlist_status(
    runlist_id: str,
    body: SetRunListStatus = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update a RunList status

    Requires: **VBR_WRITE_PUBLIC**"""
    runlist_id = sanitize_identifier_string(runlist_id)
    collection = client.get_collection_by_local_id(runlist_id)
    collection = client.update_collection_status_by_name(
        collection, status_name=body.status.value, comment=body.comment
    )
    # TODO - take any requisite actions associated with specific statuses

    query = {"runlist_id": {"operator": "eq", "value": collection.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="runlists_base", query=query, limit=1, offset=0
        )[0]
    )
    return row


# GET /{runlist_id}/events
# List event history for a RunList
@router.get(
    "/{runlist_id}/events",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[Event],
)
def get_events_for_runlist(
    runlist_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Events for a RunList.

    Requires: **VBR_READ_PUBLIC**"""
    runlist_id = sanitize_identifier_string(runlist_id)
    query = {"collection_id": {"operator": "=", "value": runlist_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="runlists_data_events_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


# GET /{runlist_id}/comments
# List comments for a RunList
@router.get(
    "/{runlist_id}/comments",
    dependencies=[Depends(vbr_read_public)],
    response_model=List[Comment],
)
def get_comments_for_runlist(
    runlist_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get Comments for a RunList.

    Requires: **VBR_READ_PUBLIC**"""
    runlist_id = sanitize_identifier_string(runlist_id)
    query = {"collection_id": {"operator": "=", "value": runlist_id}}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="runlists_comments_public",
            query=query,
            limit=0,
            offset=0,
        )
    ]
    return rows


# GPOST /{runlist_id}/comments
# Add a comment to a RunList
@router.post(
    "/{runlist_id}/comments",
    dependencies=[Depends(vbr_write_public)],
    response_model=Comment,
)
def add_runlist_comment(
    runlist_id: str,
    body: CreateComment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Add a Comment to a RunList.

    Requires: **VBR_WRITE_PUBLIC**"""
    runlist_id = sanitize_identifier_string(runlist_id)
    collection = client.get_collection_by_local_id(runlist_id)
    data_event = client.create_and_link(comment=body.comment, link_target=collection)[0]
    return Comment(comment=data_event.comment, timestamp=data_event.event_ts)
