"""VBR Location routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api

from ..dependencies import *
from .models import Location, transform

router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Location])
def list_locations(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    """List Locations.

    Requires: **VBR_READ**"""
    # TODO - build up from filters
    query = {}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="locations_public",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{location_id}", dependencies=[Depends(role_vbr_read)], response_model=Location
)
def get_location_by_id(
    location_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Location by ID.

    Requires: **VBR_READ**"""
    query = {"location_id": {"operator": "eq", "value": location_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="locations_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# TODO Later
# PUT /{location_id} - update location
# POST / - create new location
