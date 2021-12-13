"""VBR Container routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api

from ..dependencies import *
from .models import Container, transform

router = APIRouter(
    prefix="/containers",
    tags=["containers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Container])
def list_containers(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    """List Containers.

    Requires: **VBR_READ**"""
    # TODO - build up from filters
    query = {}
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
    "/{container_id}", dependencies=[Depends(role_vbr_read)], response_model=Container
)
def get_container_by_id(
    container_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Container by ID.

    Requires: **VBR_READ**"""
    query = {"container_id": {"operator": "eq", "value": container_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="containers_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.get(
    "/tracking/{tracking_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Container,
)
def get_container_by_tracking_id(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Container by tracking ID.

    Requires: **VBR_READ**"""
    query = {"container_tracking_id": {"operator": "eq", "value": tracking_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="containers_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# TODO
# PUT /{container_id}/status - update status by status.name
# PUT /{container_id}/location - update location by location_id
# GET /{container_id}/history
# GET /{container_id}/comments
# POST /{container_id}/comments
# TODO Later
# POST / - create new container
