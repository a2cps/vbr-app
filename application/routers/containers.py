"""VBR Units"""
from vbr.api import VBR_Api
from vbr.tableclasses import Container as ContainerRow
from fastapi import APIRouter, Body, Depends, HTTPException

from application.routers.models.actions import location
from ..dependencies import *
from .models import Container, ContainerTable, CreateContainer
from .builders import build_container
from .models.tables import build_container_table

router = APIRouter(
    prefix="/containers",
    tags=["containers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Container])
def containers(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "container", limit=common["limit"], offset=common["offset"]
        )
    ]
    containers = [build_container(row, client) for row in rows]
    return containers


@router.post("/", dependencies=[Depends(role_vbr_write)], response_model=Container)
def create_container(
    body: CreateContainer = Body(...),
    client: VBR_Api = Depends(vbr_admin_client),
):
    data = body.dict()
    # Lookup local_ids and transform into _pkids
    # TODO - consider making this an vbr.api
    parent_local_id = data.pop("parent_container_local_id", None)
    location_local_id = data.pop("location_local_id", None)
    if parent_local_id is not None:
        data["parent_id"] = client.get_container_by_local_id(
            parent_local_id
        ).primary_key_id()
    if location_local_id is not None:
        data["location_id"] = client.get_location_by_local_id(
            location_local_id
        ).primary_key_id()

    # TODO - this should not be hard-coded. Replace once container_type gains local_id and we've implemented a container_types listing
    data["container_type_id"] = 1
    data["project_id"] = 1
    resp = client.create_container(**data)
    return build_container(resp, client)


@router.get(
    "/table",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[ContainerTable],
)
def container_tables(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "container", limit=common["limit"], offset=common["offset"]
        )
    ]
    containers = [build_container(row, client) for row in rows]
    container_tables = [build_container_table(cont, client) for cont in containers]
    return container_tables
