"""VBR Units"""
from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api

from ..dependencies import *
from .builders import build_location
from .models import CreateLocation, Location

router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{location_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Location],
)
def location(
    location_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    loc = client.get_location_by_local_id(location_id)
    return build_location(loc, client)


@router.put(
    "/{location_id}", dependencies=[Depends(role_vbr_write)], response_model=Location
)
def update_location(
    location_id: str,
    body: CreateLocation = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    loc = client.get_location_by_local_id(location_id)
    data = body.dict()
    for k, v in data.items:
        setattr(loc, k, v)
    resp = client.vbr_client.update_row(loc)
    return build_location(resp, client)
