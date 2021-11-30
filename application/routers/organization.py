"""VBR Units"""
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
    "/{name}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Organization,
)
def organization(
    name: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    loc = client.get_organization_by_name(name)
    return build_organization(loc, client)
