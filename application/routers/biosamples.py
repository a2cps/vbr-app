"""VBR Units"""
from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api

from ..dependencies import *
from .builders import build_biosample
from .models import Biosample

router = APIRouter(
    prefix="/biosamples",
    tags=["biosamples"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Biosample])
def get_biosamples(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "biosample", limit=common["limit"], offset=common["offset"]
        )
    ]
    biosamples = [build_biosample(row, client) for row in rows]
    return biosamples
