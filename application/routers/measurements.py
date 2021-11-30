"""VBR Units"""
from vbr.api import VBR_Api
from fastapi import APIRouter, Body, Depends, HTTPException

from application.routers.models.actions import comment, measurement
from ..dependencies import *
from .models import Measurement, MeasurementTable, BulkChangeMeasurementContainer
from .models import build_measurement_table
from .builders import build_measurement

router = APIRouter(
    prefix="/measurements",
    tags=["measurements"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/", dependencies=[Depends(role_vbr_read)], response_model=List[Measurement]
)
def measurements(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "measurement", limit=common["limit"], offset=common["offset"]
        )
    ]
    measurements = [build_measurement(row, client) for row in rows]
    return measurements


@router.get(
    "/table",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[MeasurementTable],
)
def measurement_tables(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "measurement", limit=common["limit"], offset=common["offset"]
        )
    ]
    measurements = [build_measurement(row, client) for row in rows]
    measurement_tables = [
        build_measurement_table(meas, client) for meas in measurements
    ]
    return measurement_tables


# router.put
# Relocate measurements in bulk
# measurements: List[measurement.local_id]
# container
@router.put(
    "/container",
    dependencies=[Depends(role_vbr_write)],
    response_model=List[Measurement],
)
def bulk_update_measurements_container(
    body: BulkChangeMeasurementContainer = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Update Container for multiple Measurements at once."""
    container = client.get_container_by_local_id(body.local_id)
    measurements = []
    response = []
    for m1 in body.measurement_local_ids:
        measurements.append(client.get_measurement_by_local_id(m1))
    for m2 in measurements:
        meas = client.relocate_measurement(m2, container, comment=body.comment)
        response.append(build_measurement(meas, client))
    return response
