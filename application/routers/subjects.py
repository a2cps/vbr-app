"""VBR Subject routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api
from vbr.utils.barcode import (generate_barcode_string,
                               sanitize_identifier_string)

from ..dependencies import *
from .models import Subject, SubjectPrivate, SubjectPrivateExtended, transform

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(vbr_read_public)], response_model=List[Subject])
def list_subjects(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    """List Subjects.

    Requires: **VBR_READ_PUBLIC**"""
    # TODO - build up from filters
    query = {}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="subjects_public",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/private",
    dependencies=[Depends(vbr_read_limited_phi)],
    response_model=List[SubjectPrivate],
)
def list_subjects_with_limited_phi(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    """List Subjects including limited PHI.

    Requires: **VBR_READ_ANY_PHI**"""
    query = {}
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="subjects_private",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows


@router.get(
    "/{subject_id}", dependencies=[Depends(vbr_read_public)], response_model=Subject
)
def get_subject_by_id(
    subject_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Subject by ID.

    Requires: **VBR_READ_PUBLIC**"""
    query = {"subject_id": {"operator": "eq", "value": subject_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="subjects_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.get(
    "/guid/{subject_guid}",
    dependencies=[Depends(vbr_read_public)],
    response_model=Subject,
)
def get_subject_by_guid(
    subject_guid: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Subject by assigned GUID.

    Requires: **VBR_READ_PUBLIC**"""
    subject_guid = sanitize_identifier_string(subject_guid)
    query = {"subject_guid": {"operator": "eq", "value": subject_guid}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="subjects_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


@router.get(
    "/{subject_id}/private",
    dependencies=[Depends(vbr_read_any_phi)],
    response_model=SubjectPrivateExtended,
)
def get_subject_by_id_with_extended_phi(
    subject_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    """Get a Subject with extended PHI by ID.

    Requires: **VBR_READ_ANY_PHI**"""
    query = {"subject_id": {"operator": "eq", "value": subject_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="subjects_private", query=query, limit=1, offset=0
        )[0]
    )
    return row


# TODO
# PUT /{subject_id}/subject_guid update tracking ID
# GET /{subject_id}/history
# GET /{subject_id}/comments
# POST /{subject_id}/comments
