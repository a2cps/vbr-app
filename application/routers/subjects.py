"""VBR Subjects Routes"""
from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api

from ..dependencies import *
from .builders import build_subject
from .models import (
    Subject,
    SubjectTable,
    SubjectTableRestricted,
    build_subject_table,
    build_subject_table_restricted,
)

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(role_vbr_read)], response_model=List[Subject])
def subjects(client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "subject", limit=common["limit"], offset=common["offset"]
        )
    ]
    subjects = [build_subject(row.subject_id, client) for row in rows]
    return subjects


@router.get(
    "/table",
    dependencies=[Depends(role_vbr_read)],
    response_model=List[SubjectTable],
)
def subject_tables(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "subject", limit=common["limit"], offset=common["offset"]
        )
    ]
    subjects = [build_subject(row.subject_id, client) for row in rows]
    subject_tables = [build_subject_table(subj, client) for subj in subjects]
    return subject_tables


@router.get(
    "/table/restricted",
    dependencies=[Depends(role_vbr_read_any)],
    response_model=List[SubjectTableRestricted],
)
def subject_restricted_tables(
    client: VBR_Api = Depends(vbr_admin_client), common=Depends(limit_offset)
):
    rows = [
        c
        for c in client.vbr_client.list_rows(
            "subject", limit=common["limit"], offset=common["offset"]
        )
    ]
    subjects = [build_subject(row, client) for row in rows]
    subject_tables = [build_subject_table_restricted(subj, client) for subj in subjects]
    return subject_tables
