"""VBR Biospecimen routes"""
from typing import Dict

from fastapi import APIRouter, Body, Depends, HTTPException
from vbr.api import VBR_Api, measurement
from vbr.utils.barcode import generate_barcode_string, sanitize_identifier_string

from application.routers.models.actions import comment, trackingid

from ..dependencies import *
from .models import (
    GenomicsSubjectsPrivate,
    transform,
)

from .utils import parameters_to_query

router = APIRouter(
    prefix="/genomics_subjects",
    tags=["genomics_subjects"],
    responses={404: {"description": "Not found"}},
    route_class=LoggingRoute,
)


@router.get(
    "/", dependencies=[Depends(vbr_read_any_phi)], response_model=List[GenomicsSubjectsPrivate]
)
def list_genomics_subject_02(
    # See views/biospecimens_details.sql for possible filter names
    src_subject_id: Optional[str] = None,
    interview_date: Optional[datetime] = None,
    interview_age: Optional[int] = None,
    sex: Optional[str] = None,
    race: Optional[str] = None,
    ethnicity: Optional[str] = None,
    phenotype: Optional[str] = None,
    twins_study: Optional[str] = None,
    sibling_study: Optional[str] = None,
    family_study: Optional[str] = None,
    sample_taken: Optional[str] = None,
    client: VBR_Api = Depends(vbr_admin_client),
    common=Depends(limit_offset),
):
    """List Genomics Subjects.

    Refine results using filter parameters.

    Requires: **VBR_READ_PUBLIC**"""
    query = parameters_to_query(
        src_subject_id=src_subject_id,
        interview_date=interview_date,
        interview_age=interview_age,
        sex=sex,
        race=race,
        ethnicity=ethnicity,
        phenotype=phenotype,
        twins_study=twins_study,
        sibling_study=sibling_study,
        family_study=family_study,
        sample_taken=sample_taken
    )
    rows = [
        transform(c)
        for c in client.vbr_client.query_view_rows(
            view_name="genomics_subjects_02",
            query=query,
            limit=common["limit"],
            offset=common["offset"],
        )
    ]
    return rows

