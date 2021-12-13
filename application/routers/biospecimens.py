"""VBR Biospecimen routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api

from ..dependencies import *
from .models import (
    Biospecimen,
    BiospecimenPrivate,
    BiospecimenPrivateExtended,
    transform,
)

router = APIRouter(
    prefix="/biospecimens",
    tags=["biospecimens"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/", dependencies=[Depends(role_vbr_read)], response_model=List[Biospecimen]
)
def list_biospecimens(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    """List Biospecimens.

    Requires: **VBR_READ**"""
    # TODO - build up from filters
    query = {}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="biospecimens_details",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/private",
    dependencies=[Depends(role_vbr_read_any)],
    response_model=List[BiospecimenPrivate],
)
def list_biospecimens_with_limited_phi(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    """List Biospecimens with limited PHI.

    Requires: **VBR_READ_ANY**"""
    # TODO - build up from filters
    query = {}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="biospecimens_details_private",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{biospecimen_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Biospecimen,
)
def get_biospecimen_by_id(
    biospecimen_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Biospecimen by ID.

    Requires: **VBR_READ**"""
    query = {"biospecimen_id": {"operator": "eq", "value": biospecimen_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.get(
    "/tracking/{tracking_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Biospecimen,
)
def get_biospecimen_by_id(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Biospecimen by Tracking ID.

    Requires: **VBR_READ**"""
    query = {"tracking_id": {"operator": "eq", "value": tracking_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.get(
    "/{biospecimen_id}/private",
    dependencies=[Depends(role_vbr_read_any)],
    response_model=BiospecimenPrivateExtended,
)
def get_biospecimen_by_id_with_extended_phi(
    biospecimen_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Biospecimen with extended PHI by ID.

    Requires: **VBR_READ_ANY**"""
    query = {"biospecimen_id": {"operator": "eq", "value": biospecimen_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="biospecimens_details_private", query=query, limit=1, offset=0
        )[0]
    )
    return row


# TODO
# PUT /{biospecimen_id}/tracking_id tracking_id
# PUT /{biospecimen_id}/container container_id
# PUT /{biospecimen_id}/status status.name, comment
# PUT /{biospecimen_id}/comments comment
# GET /{biospecimen_id}/history
# GET /{biospecimen_id}/comments
# POST /{biospecimen_id}/comments
# TODO Later
# POST /partition - partition a biospecimen into two
