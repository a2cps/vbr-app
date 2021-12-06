"""VBR Locations Routes"""
from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api
from vbr.tableclasses import Location as LocationRow

from ..dependencies import *
from .builders import build_location
from .models import CreateLocation, Location

router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Location])
def locations(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "location", limit=common["limit"], offset=common["offset"]
        )
    ]
    locations = [build_location(row, client) for row in rows]
    return locations


@router.post("/", dependencies=[Depends(role_vbr_write)], response_model=Location)
def create_location(
    body: CreateLocation = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    data = body.dict()
    row = LocationRow(**data)
    resp = client.vbr_client.create_row(row)[0]
    return Location(**resp.dict())
