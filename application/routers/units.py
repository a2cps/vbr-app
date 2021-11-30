"""VBR Units"""
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import *

router = APIRouter(
    prefix="/units",
    tags=["units"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(role_vbr_read)])
def get_units(client: Tapis = Depends(tapis_admin_client)):
    return [
        c.__dict__
        for c in client.pgrest.get_table(collection="unit", limit=1000, offset=0)
    ]
