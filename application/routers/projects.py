"""VBR Project routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api
from vbr.utils.barcode import (generate_barcode_string,
                               sanitize_identifier_string)

from ..dependencies import *
from .models import Project, transform
from .utils import parameters_to_query

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(vbr_read_public)], response_model=List[Project])
def list_projects(
    # See views/projects_public.sql for possible filter names
    project_id: Optional[str] = None,
    name: Optional[str] = None,
    abbreviation: Optional[str] = None,
    description: Optional[str] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List Projects.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    # TODO - build up from filters
    query = parameters_to_query(
        project_id=project_id,
        name=name,
        abbreviation=abbreviation,
        description=description,
    )
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="projects_public",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{project_id}", dependencies=[Depends(vbr_read_public)], response_model=Project
)
def get_project_by_id(
    project_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Project by ID.

    Requires: **VBR_READ_PUBLIC**"""
    query = {"project_id": {"operator": "eq", "value": project_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="projects_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# TODO
# PUT /{project_id} - update project
# POST / - create new project
