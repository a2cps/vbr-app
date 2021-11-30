"""VBR Organizations"""
from vbr.api import VBR_Api
from fastapi import APIRouter, Body, Depends, HTTPException
from ..dependencies import *
from .models import Organization
from .builders import build_organization

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/", dependencies=[Depends(role_vbr_read)], response_model=List[Organization]
)
def organizations(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "organization", limit=common["limit"], offset=common["offset"]
        )
    ]
    organizations = [build_organization(row, client) for row in rows]
    return organizations


# No add/edits
