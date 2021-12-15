"""VBR Organization routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api
from vbr.utils.barcode import (generate_barcode_string,
                               sanitize_identifier_string)

from ..dependencies import *
from .models import Organization, transform
from .utils import parameters_to_query

router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/", dependencies=[Depends(vbr_read_public)], response_model=List[Organization]
)
def list_organizations(
    # See views/organizations_public.sql for possible filter names
    organization_id: Optional[str] = None,
    name: Optional[str] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List Organizations.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    query = parameters_to_query(organization_id=organization_id, name=name)
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="organizations_public",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{organization_id}",
    dependencies=[Depends(vbr_read_public)],
    response_model=Organization,
)
def get_organization_by_id(
    organization_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Organization by ID.

    Requires: **VBR_READ_PUBLIC**"""
    query = {"organization_id": {"operator": "eq", "value": organization_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="organizations_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# TODO Later
# PUT /{organization_id} - update organization
# POST / - create new organization
