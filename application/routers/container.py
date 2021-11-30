"""VBR Units"""
from vbr.api import VBR_Api
from fastapi import APIRouter, Body, Depends, HTTPException

from application.routers.models.actions import comment
from application.routers.models.vbr.multiple import Measurement
from ..dependencies import *
from .models import (
    Container,
    Comment,
    CreateComment,
    DataEvent,
    SetTrackingId,
    SetLocationLocalId,
    SetContainerStatus,
)
from .builders import (
    build_container,
    build_location,
    build_measurement,
    build_data_event,
)

router = APIRouter(
    prefix="/containers",
    tags=["containers"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{tracking_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Container,
)
def container_by_tracking_id(
    tracking_id: str, client: VBR_Api = Depends(vbr_admin_client)
):
    cont = client.get_container_by_tracking_id(tracking_id)
    return build_container(cont, client)


# Admin actions are by local ID only
@router.get(
    "/{local_id}",
    dependencies=[Depends(role_vbr_read)],
    response_model=Container,
)
def container(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    cont = client.get_container_by_local_id(local_id)
    return build_container(cont, client)


@router.get(
    "/{local_id}/children",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Container],
)
def get_container_children(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """List Container immediate children."""
    container = client.get_container_by_local_id(local_id)
    container_children = client.get_container_children(container, recursive=False)
    return [build_container(cont, client) for cont in container_children]


@router.get(
    "/{local_id}/descendants",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Container],  # TODO - need a tree structure
)
def get_container_descendants(
    local_id: str, client: VBR_Api = Depends(vbr_admin_client)
):
    """Recursively list all Container children."""
    container = client.get_container_by_local_id(local_id)
    container_children = client.get_container_children(container, recursive=True)
    return [build_container(cont, client) for cont in container_children]


@router.get(
    "/{local_id}/parent",
    dependencies=[Depends(role_vbr_read)],
    response_model=Container,
)
def get_container_parent(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """Get Container immediate parent."""
    container = client.get_container_by_local_id(local_id)
    container_parent = client.get_container_parent(container)
    return build_container(container_parent, client)


@router.get(
    "/{local_id}/ancestors",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Container],
)
def get_container_ancestors(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """Get Container complete parental lineage."""
    container = client.get_container_by_local_id(local_id)
    container_parents = client.get_container_lineage(container)
    return [build_container(parent, client) for parent in container_parents]


@router.get(
    "/{local_id}/measurements",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Measurement],
)
def list_container_measurements(
    local_id: str, recursive: bool = True, client: VBR_Api = Depends(vbr_admin_client)
):
    """List Measurements in the specified Container."""
    container = client.get_container_by_local_id(local_id)
    if recursive:
        # TODO - add in recursive=True when API supports it
        children = client.get_container_children(container)
    else:
        children = []
    containers = [container]
    measurements = []
    containers.extend(children)
    for cont in containers:
        measurements.extend(
            [
                build_measurement(m, client)
                for m in client.get_measurements_in_container(cont)
            ]
        )
    return measurements


@router.get(
    "/{local_id}/history",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[DataEvent],
)
def container_history(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """Get Container event history."""
    # TODO - implement filters
    cont = client.get_container_by_local_id(local_id)
    data_events = client.data_events_for_record(cont)
    return [build_data_event(de, client) for de in data_events]


@router.get(
    "/{local_id}/comments",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[Comment],
)
def container_comments(local_id: str, client: VBR_Api = Depends(vbr_admin_client)):
    """Get Container comments"""
    cont = client.get_container_by_local_id(local_id)
    data_events = client.data_events_for_record(cont)
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
def add_container_comment(
    local_id: str,
    body: CreateComment = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Add a comment to a Container."""
    cont = client.get_container_by_local_id(local_id)
    data_event = client.create_and_link(comment=body.comment, link_target=cont)[0]
    return Comment(comment=data_event.comment, event_ts=data_event.event_ts)


@router.put(
    "/{local_id}/tracking_id",
    dependencies=[Depends(role_vbr_write)],
    response_model=Container,
)
def update_container_tracking_id(
    local_id: str,
    body: SetTrackingId = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Update a Container's tracking ID"""
    # TODO - Propagate the comment
    cont = client.relabel_container_by_local_id(local_id, body.tracking_id)
    return build_container(cont, client)


@router.put(
    "/{local_id}/location",
    dependencies=[Depends(role_vbr_write)],
    response_model=Container,
)
def update_container_location(
    local_id: str,
    body: SetLocationLocalId = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update a Container's location"""
    # TODO - check that this syncs to children
    cont = client.relocate_container_by_local_id(local_id, body.local_id)
    return build_container(cont, client)


@router.put(
    "/{local_id}/parent",
    dependencies=[Depends(role_vbr_write)],
    response_model=Container,
)
def update_container_parent(
    local_id: str,
    # TODO Write this code
    body: SetLocationLocalId = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update a Container's parent"""
    # TODO Write this code
    # TODO Un-nest by allowing null for parent
    # TODO - check that this syncs to children
    cont = client.relocate_container_by_local_id(local_id, body.local_id)
    return build_container(cont, client)


@router.put(
    "/{local_id}/status",
    dependencies=[Depends(role_vbr_write)],
    response_model=Container,
)
def update_container_status(
    local_id: str,
    body: SetContainerStatus = Body(...),
    client: Tapis = Depends(vbr_admin_client),
):
    """Update a Container's status"""
    # raise SystemError(status_name)
    cont = client.get_container_by_local_id(local_id)
    container = client.update_container_status_by_name(
        cont, status_name=body.status.value, comment=body.comment
    )
    return build_container(container, client)
