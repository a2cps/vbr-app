"""VBR Units"""
from vbr.api import VBR_Api
from fastapi import APIRouter, Body, Depends, HTTPException
from ..dependencies import *
from .models import (
    Comment,
    CreateComment,
    Subject,
    SubjectTable,
    SubjectTableRestricted,
)
from .models.actions import SetTrackingId, TrackingId
from .models import build_subject_table, build_subject_table_restricted
from .builders import build_subject

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{guid}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Subject,
)
def subject_by_guid(guid: str, client: VBR_Api = Depends(vbr_admin_client)):
    meas = client.get_subject_by_tracking_id(guid)
    return build_subject(meas, client)


@router.get(
    "/{guid_id}/table",
    dependencies=[Depends(role_vbr_read)],
    response_model=SubjectTable,
)
def subject_table_by_guid(guid: str, client: VBR_Api = Depends(vbr_admin_client)):
    meas = client.get_subject_by_tracking_id(guid)
    meas_data = build_subject(meas, client)
    return build_subject_table(meas_data, client)


@router.get(
    "/{guid}/table/restricted",
    dependencies=[Depends(role_vbr_read_any)],
    response_model=SubjectTableRestricted,
)
def subject_restricted_table_by_guid(
    guid: str, client: VBR_Api = Depends(vbr_admin_client)
):
    meas = client.get_subject_by_tracking_id(guid)
    meas_data = build_subject(meas, client)
    return build_subject_table_restricted(meas_data, client)


# Admin actions are by local ID only
@router.get(
    "/{local_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Subject,
)
def subject(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    meas = client.get_subject_by_local_id(local_id)
    return build_subject(meas, client)


@router.get(
    "/{local_id}/comments",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Comment],
)
def subject_comments(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """Get Subject comments"""
    subj = client.get_subject_by_local_id(local_id)
    data_events = client.data_events_for_record(subj)
    return [
        {"event_ts": de.event_ts, "comment": de.comment}
        for de in data_events
        if de.comment is not None
    ]


@router.post(
    "/{local_id}/comments",
    dependencies=[Depends(role_vbr_write)],
    response_model=Comment,
)
def add_subject_comment(
    local_id: str,
    body: CreateComment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Add a comment to a Subject."""
    subj = client.get_subject_by_local_id(local_id)
    data_event = client.create_and_link(comment=body.comment, link_target=subj)[0]
    return Comment(comment=data_event.comment, event_ts=data_event.event_ts)


@router.put(
    "/{local_id}/tracking_id",
    dependencies=[Depends(role_vbr_write_any)],
    response_model=TrackingId,
)
def update_subject_tracking_id(
    local_id: str,
    body: SetTrackingId = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Change a Subject's tracking ID

    Requires XXX role.
    """
    # TODO - Propagate the comment
    subj = client.relabel_subject(local_id, body.tracking_id)
    tracking_id = TrackingId(tracking_id=subj.tracking_id)
    return tracking_id
