"""VBR RunListroutes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api, tracking_id
from vbr.utils.barcode import generate_barcode_string, sanitize_identifier_string

# from application.routers import container_types
from application.routers.models.actions.comment import Comment
from application.routers.models.actions.runlist import CreateRunList

from ..dependencies import *
from .models import (
    AddBiospecimen,
    Biospecimen,
    CreateComment,
    Event,
    SetRunListStatus,
    RunList,
    transform,
)
from .utils import parameters_to_query

router = APIRouter(
    prefix="/runlists",
    tags=["runlists"],
    responses={404: {"description": "Not found"}},
    route_class=LoggingRoute,
)


@router.get("/", dependencies=[Depends(vbr_read_public)], response_model=List[RunList])
def list_runlists(
    # See views/runlists_base.sql for possible filter names
    runlist_id: Optional[str] = None,
    tracking_id: Optional[str] = None,
    name: Optional[str] = None,
    status_name: Optional[str] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List RunLists.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    query = parameters_to_query(
        runlist_id=runlist_id,
        tracking_id=tracking_id,
        name=name,
        status_name=status_name,
    )
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="runlists_base",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows
