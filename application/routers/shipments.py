"""VBR Shipment routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api

from ..dependencies import *
from .models import Shipment, transform

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(vbr_read_public)], response_model=List[Shipment])
def list_shipments(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    """List Shipments.

    Requires: **VBR_READ**"""
    # TODO - build up from filters
    query = {}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="shipments_public",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{shipment_id}", dependencies=[Depends(vbr_read_public)], response_model=Shipment
)
def get_shipment_by_id(
    shipment_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Shipment by ID.

    Requires: **VBR_READ**"""
    query = {"shipment_id": {"operator": "eq", "value": shipment_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="shipments_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.get(
    "/tracking/{tracking_id}",
    dependencies=[Depends(vbr_read_public)],
    response_model=Shipment,
)
def get_shipment_by_tracking_id(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Shipment by parcel tracking ID.

    Requires: **VBR_READ**"""
    query = {"tracking_id": {"operator": "eq", "value": tracking_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="shipments_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# TODO
# PUT /{shipment_id}/status - update status by status.name
# GET /{shipment_id}/history
# GET /{shipment_id}/comments
# POST /{shipment_id}/comments
# TODO Later
# POST / - create new shipment
