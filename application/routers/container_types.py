"""VBR ContainerType routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api
from vbr.utils.barcode import generate_barcode_string, sanitize_identifier_string

from ..dependencies import *
from .models import ContainerType, CreateContainerType, GenericResponse, transform
from .utils import parameters_to_query

router = APIRouter(
    prefix="/container_types",
    tags=["container_types"],
    responses={404: {"description": "Not found"}},
    route_class=LoggingRoute,
)


@router.get(
    "/", dependencies=[Depends(vbr_read_public)], response_model=List[ContainerType]
)
def list_container_types(
    # See views/container_types_public.sql for possible filter names
    container_type_id: Optional[str] = None,
    name: Optional[str] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List ContainerTypes.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    query = parameters_to_query(container_type_id=container_type_id, name=name)
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="container_types_public",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{container_type_id}",
    dependencies=[Depends(vbr_read_public)],
    response_model=ContainerType,
)
def get_container_type_by_id(
    container_type_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a ContainerType by ID.

    Requires: **VBR_READ_PUBLIC**"""
    query = {"container_type_id": {"operator": "eq", "value": container_type_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="container_types_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# POST /
@router.post(
    "/", dependencies=[Depends(vbr_write_public)], response_model=ContainerType
)
def create_container_type(
    body: CreateContainerType = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Create a new ContainerType.

    Requires: **VBR_WRITE_PUBLIC**
    """

    try:
        container_type = client.create_container_type(
            name=body.name, description=body.description
        )
    except Exception as exc:
        raise HTTPException(500, "Failed to create new container type: {0}".format(exc))

    query = {"container_type_id": {"operator": "eq", "value": container_type.local_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="container_types_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# DELETE /{container_type_id}
@router.delete(
    "/{container_type_id}",
    dependencies=[Depends(vbr_admin)],
    response_model=GenericResponse,
)
def delete_container_type(
    container_type_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Delete a ContainerType.

    Requires: **VBR_ADMIN**"""
    container_type_id = vbr.utils.sanitize_identifier_string(container_type_id)
    container_type = client.get_container_type_by_local_id(container_type_id)
    client.vbr_client.delete_row(container_type)
    return {"message": "ContainerType deleted"}


# TODO Later
# PUT /{container_type_id} - update container_type
