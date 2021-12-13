"""VBR Subject routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api

from ..dependencies import *
from .models import Subject, SubjectPrivate, SubjectPrivateExtended, transform

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
    responses={404: {"description": "Not found"}},
)


# @router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Dict])
@router.get("/", dependencies=[], response_model=List[Subject])
def list_subjects(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
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


# @router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Dict])
@router.get("/private", dependencies=[], response_model=List[SubjectPrivate])
def list_subjects_with_biological_sex(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    # TODO - build up from filters
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


# @router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Dict])
@router.get("/{subject_id}", dependencies=[], response_model=Subject)
def get_subject_by_id(
    subject_id: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    query = {"subject_id": {"operator": "eq", "value": subject_id}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="subjects_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# @router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Dict])
@router.get("/guid/{subject_guid}", dependencies=[], response_model=Subject)
def get_subject_by_guid(
    subject_guid: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    query = {"subject_guid": {"operator": "eq", "value": subject_guid}}
    row = transform(
        client.vbr_client.query_view_rows(
            view_name="subjects_public", query=query, limit=1, offset=0
        )[0]
    )
    return row


# @router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Dict])
@router.get(
    "/guid/{subject_guid}/private",
    dependencies=[],
    response_model=SubjectPrivateExtended,
)
def get_subject_private_info_by_guid(
    subject_guid: str,
    client: VBR_Api = Depends(vbr_admin_client),
):
    query = {"subject_guid": {"operator": "eq", "value": subject_guid}}
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
