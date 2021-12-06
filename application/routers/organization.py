"""VBR Organization Routes"""
from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api

from ..dependencies import *
from .builders import build_organization
from .models import Organization

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/name/{name}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Organization,
)
def organization(
    name: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    loc = client.get_organization_by_name(name)
    return build_organization(loc, client)


# TODO - add support for /{local_id} when it is live in the database and Python API
