"""VBR Unit routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api
from vbr.utils.barcode import generate_barcode_string, sanitize_identifier_string

from ..dependencies import *
from .models import Unit, transform
from .utils import parameters_to_query

router = APIRouter(
    prefix="/units",
    tags=["units"],
    responses={404: {"description": "Not found"}},
    route_class=LoggingRoute,
)


@router.get("/", dependencies=[Depends(vbr_read_public)], response_model=List[Unit])
def list_units(
    # See views/units_public.sql for possible filter names
    unit_id: Optional[str] = None,
    name: Optional[str] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List Units.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    query = parameters_to_query(unit_id=unit_id, name=name)
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="units_public",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{unit_id}",
    dependencies=[Depends(vbr_read_public)],
    response_model=Unit,
)
def get_unit_by_id(
    unit_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Unit by ID.

    Requires: **VBR_READ_PUBLIC**"""
    query = {"unit_id": {"operator": "eq", "value": unit_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="units_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# TODO Later
# PUT /{unit_id} - update unit
# POST / - create new unit
