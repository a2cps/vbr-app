"""VBR Units"""
from vbr.api import VBR_Api
from fastapi import APIRouter, Body, Depends, HTTPException

from application.routers.models.actions import tracking_id

from ..dependencies import *
from .models import (
    Comment,
    CreateComment,
    Measurement,
    MeasurementTable,
    SetTrackingId,
    ChangeMeasurementContainer,
    PartitionMeasurement,
    PartitionedMeasurement,
)
from .models import build_measurement_table
from .builders import build_measurement

router = APIRouter(
    prefix="/measurements",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{local_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Measurement,
)
def measurement(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    meas = client.get_measurement_by_local_id(local_id)
    return build_measurement(meas, client)


@router.get(
    "/{local_id}/table",
    dependencies=[Depends(role_vbr_read)],
    response_model=MeasurementTable,
)
def measurement_table(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    meas = client.get_measurement_by_local_id(local_id)
    meas_data = build_measurement(meas, client)
    return build_measurement_table(meas_data, client)


@router.get(
    "/{local_id}/comments",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Comment],
)
def measurement_comments(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """Get Measurement comments"""
    meas = client.get_measurement_by_local_id(local_id)
    data_events = client.data_events_for_record(meas)
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
def add_measurement_comment(
    local_id: str,
    body: CreateComment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Add a comment to a Measurement."""
    meas = client.get_measurement_by_local_id(local_id)
    data_event = client.create_and_link(comment=body.comment, link_target=meas)[0]
    return Comment(comment=data_event.comment, event_ts=data_event.event_ts)


@router.put(
    "/{local_id}/container",
    dependencies=[Depends(role_vbr_write)],
    response_model=Measurement,
)
def update_measurement_container(
    local_id: str,
    body: ChangeMeasurementContainer = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Change a Measurement's Container"""
    # TODO - Propagate the comment
    # TODO - ACTUALLY WRITE THE PYTHON API METHOD: relocate measurement
    meas = client.relabel_measurement(local_id, body.tracking_id)
    return build_measurement(meas, client)


@router.post(
    "/{local_id}/partition",
    dependencies=[Depends(role_vbr_write)],
    response_model=PartitionedMeasurement,
)
def partition_measurement(
    local_id: str,
    body: PartitionMeasurement = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Subdivide an aliquot from a Measurement"""
    meas = client.get_measurement_by_local_id(local_id)
    aliq = client.partition_measurement(
        meas, tracking_id=body.tracking_id, comment=body.comment
    )
    source = build_measurement(meas, client)
    aliquot = build_measurement(aliq, client)
    return PartitionedMeasurement(source=source, aliquot=aliquot)


# TODO - Update a Measurement's status
@router.put(
    "/{local_id}/status",
    dependencies=[Depends(role_vbr_write)],
    response_model=Measurement,
)
def update_measurement_status(
    local_id: str,
    # TODO Write this code
    body: SetTrackingId = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Change a Measurement's status"""
    # TODO Write this code
    meas = client.relabel_measurement(local_id, body.tracking_id)
    return build_measurement(meas, client)


@router.put(
    "/{local_id}/tracking_id",
    dependencies=[Depends(role_vbr_write)],
    response_model=Measurement,
)
def update_measurement_tracking_id(
    local_id: str,
    body: SetTrackingId = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Change a Measurement's tracking ID"""
    # TODO - Propagate the comment
    meas = client.relabel_measurement(local_id, body.tracking_id)
    return build_measurement(meas, client)
