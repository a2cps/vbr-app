"""VBR RunlistType routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api
from vbr.utils.barcode import generate_barcode_string, sanitize_identifier_string

from ..dependencies import *
from .models import CreateRunlistType, RunlistType, GenericResponse, transform
from .utils import parameters_to_query

router = APIRouter(
    prefix="/runlist_types",
    tags=["runlist_types"],
    responses={404: {"description": "Not found"}},
    route_class=LoggingRoute,
)


@router.get(
    "/", dependencies=[Depends(vbr_read_public)], response_model=List[RunlistType]
)
def list_runlist_types(
    # See views/runlist_types_public.sql for possible filter names
    runlist_type_id: Optional[str] = None,
    name: Optional[str] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List RunlistTypes.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    query = parameters_to_query(runlist_type_id=runlist_type_id, name=name)
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="runlist_types_public",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{runlist_type_id}",
    dependencies=[Depends(vbr_read_public)],
    response_model=RunlistType,
)
def get_runlist_type_by_id(
    runlist_type_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a RunlistType by ID.

    Requires: **VBR_READ_PUBLIC**"""
    query = {"runlist_type_id": {"operator": "eq", "value": runlist_type_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="runlist_types_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# POST /
@router.post("/", dependencies=[Depends(vbr_write_public)], response_model=RunlistType)
def create_runlist_type(
    body: CreateRunlistType = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Create a new RunlistType.

    Requires: **VBR_WRITE_PUBLIC**
    """

    try:
        runlist_type = client.create_collection_type(
            name=body.name, description=body.description
        )
    except Exception as exc:
        raise HTTPException(500, "Failed to create new container type: {0}".format(exc))

    query = {"runlist_type_id": {"operator": "eq", "value": runlist_type.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="runlist_types_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# DELETE /{runlist_type_id}
@router.delete(
    "/{runlist_type_id}",
    dependencies=[Depends(vbr_admin)],
    response_model=GenericResponse,
)
def delete_runlist_type(
    runlist_type_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Delete a RunlistType.

    Requires: **VBR_ADMIN**"""
    runlist_type_id = vbr.utils.sanitize_identifier_string(runlist_type_id)
    runlist_type = client.get_collection_type_by_local_id(runlist_type_id)
    client.vbr_client.delete_row(runlist_type)
    return {"message": "RunlistType deleted"}


# TODO Later
# PUT /{runlist_type_id} - update runlist_type
