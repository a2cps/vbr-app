"""VBR Units"""
from vbr.api import VBR_Api
from fastapi import APIRouter, Body, Depends, HTTPException
from ..dependencies import *
from .models import Location, CreateLocation
from .builders import build_location

router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{local_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Location],
)
def location(
    local_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    loc = client.get_location_by_local_id(local_id)
    return build_location(loc, client)


@router.put(
    "/{local_id}", dependencies=[Depends(role_vbr_write)], response_model=Location
)
def update_location(
    local_id: str,
    body: CreateLocation = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    loc = client.get_location_by_local_id(local_id)
    data = body.dict()
    for k, v in data.items:
        setattr(loc, k, v)
    resp = client.vbr_client.update_row(loc)
    return build_location(resp, client)
