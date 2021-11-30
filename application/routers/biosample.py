"""VBR Units"""
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import Field
from vbr.api import VBR_Api

from ..dependencies import *
from .builders import build_biosample
from .models import Biosample, Comment, CreateComment, SetTrackingId, TrackingId

router = APIRouter(
    prefix="/biosamples",
    tags=["biosamples"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/tracking/{tracking_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Biosample,
)
def get_biosample_by_tracking_id(
    tracking_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """View a Biosample by Tracking ID"""
    bios = client.get_biosample_by_tracking_id(tracking_id)
    return build_biosample(bios, client)


# Admin actions are by local ID only
@router.get(
    "/{biosample_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Biosample,
)
def get_biosample(biosample_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """View a Biosample"""
    bios = client.get_biosample_by_local_id(biosample_id)
    return build_biosample(bios, client)


@router.get(
    "/{biosample_id}/comments",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Comment],
)
def biosample_comments(biosample_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """Get Biosample comments"""
    bios = client.get_biosample_by_local_id(biosample_id)
    data_events = client.data_events_for_record(bios)
    return [
        {"event_ts": de.event_ts, "comment": de.comment}
        for de in data_events
        if de.comment is not None
    ]


@router.post(
    "/{biosample_id}/comments",
    dependencies=[Depends(role_vbr_write)],
    response_model=Comment,
)
def add_biosample_comment(
    biosample_id: str,
    body: CreateComment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Add a comment to a Biosample."""
    bios = client.get_biosample_by_local_id(biosample_id)
    data_event = client.create_and_link(comment=body.comment, link_target=bios)[0]
    return Comment(comment=data_event.comment, event_ts=data_event.event_ts)


@router.put(
    "/{biosample_id}/tracking_id",
    dependencies=[Depends(role_vbr_write)],
    response_model=Biosample,
)
def update_biosample_tracking_id(
    biosample_id: str,
    body: SetTrackingId = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Change a Biosample's tracking ID"""
    # TODO - Propagate the comment
    bios = client.relabel_biosample(biosample_id, body.tracking_id)
    biosample = build_biosample(bios, client)
    return biosample
