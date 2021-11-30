from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
from vbr.api import VBR_Api
from vbr.utils.redcaptasks.time import redcap_to_datetime

__all__ = [
    "BiosampleReport",
    "build_biosample_report",
    "BiosampleReportRestricted",
    "build_biosample_report_restricted",
    "BiosampleReportQC",
    "build_biosample_report_qc",
]

MAPPINGS = {
    # Choices: 1, Male | 2, Female | 3, Unknown | 4, Intersex
    "sex": {1: "Male", 2: "Female", 3: "Unknown", 4: "Intersex"},
    # Choices: 1, American Indian or Alaska Native | 2, Asian | 3, Black or African-American | 4, Native Hawaiian or Pacific Islander | 5, White | 6, Unknown | 7, Not Reported
    "race": {
        1: "American Indian or Alaska Native",
        2: "Asian",
        3: "Black or African-American",
        4: "Native Hawaiian or Pacific Islander",
        5: "White",
        6: "Unknown",
        7: "Not Reported",
    },
    # Choices: 1, Hispanic or Latino, A person of Mexican, Puerto Rican, Cuban, Central or South American or other Spanish culture or origin, regardless of race | 2, Not Hispanic or Latino, A person not of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin, regardless of race. An arbitrary ethnic classification | 3, Unknown, Not known, not observed, not recorded, or refused | 4, Not reported, Not provided or available
    "ethnicity": {
        1: "Hispanic or Latino",
        2: "Not Hispanic or Latino",
        3: "Unknown",
        4: "Not reported",
    },
    # Choices: 1, Unable to obtain blood sample -technical reason | 2, Unable to obtain blood sample -patient related | 3, Sample handling/processing error
    "protocol_deviation_reason": {
        1: "Unable to obtain blood sample -technical reason",
        2: "Unable to obtain blood sample -patient related",
        3: "Sample handling/processing error",
    },
}


class BiosampleReport(BaseModel):
    """Report view for Biosamples"""

    local_id: str
    case_guid: UUID
    creation_time: str
    tracking_id: str
    project: str
    visit: str
    biosample_tracking_id: str
    # Derived from original blood draw CRF
    recorded_plasma_aliquot_count: int
    recorded_buffycoat_count: int
    recorded_paxgene_count: int
    # TODO - built 'actual' count field for each


class BiosampleReportRestricted(BiosampleReport):
    """Report view for Biosamples including PHI-Restricted fields"""

    # Sourced from from Demographics CRF(s)
    # Mapped from redcap values to strings using MAPPINGS above
    sex: str
    age: int
    race: str
    ethnicity: str


class BiosampleReportQC(BiosampleReportRestricted):
    """Report view for Biosamples including detailed detailed diagnotics metadata"""

    # bscp_comments
    comments: str
    # homologous level (g/L hemoglobin)
    degree_of_hemolysis: float
    # bscp_procby_initials
    processed_by: str
    # bscp_protocol_dev
    protocol_deviation: bool
    # bscp_protocol_dev_reason
    protocol_deviation_reason: Optional[str]
    # Computed
    time_to_centrifuge: str
    time_to_freeze: str


def _build_biosample_report_data(biosample_id: int, vbr_api: VBR_Api) -> dict:
    data = {}
    vbr_biosample = vbr_api._get_row_from_table_with_id("biosample", biosample_id)
    vbr_project = vbr_api._get_row_from_table_with_id("project", vbr_biosample.project)
    data["project"] = vbr_project.name
    vbr_protocol = vbr_api._get_row_from_table_with_id(
        "protocol", vbr_biosample.protocol
    )
    vbr_subject = vbr_api._get_row_from_table_with_id("subject", vbr_biosample.subject)
    query = {
        "subject_id": {"operator": "=", "value": vbr_subject.subject_id},
        "protocol_id": {"operator": "=", "value": vbr_protocol.protocol_id},
    }
    blood_draw_crfs = vbr_api._get_rows_from_table_with_query(
        "rcap_blood_sample_collection_and_processing_crf", query=query
    )
    blood_draw_crf = blood_draw_crfs[0]
    # Comments
    data["comments"] = getattr(blood_draw_crf, "bscp_comments", "")
    # Hemolysis
    data["degree_of_hemolysis"] = float(blood_draw_crf.bscp_deg_of_hemolysis)
    data["recorded_plasma_aliquot_count"] = int(blood_draw_crf.bscp_aliq_cnt)
    # TODO - set these to ZERO if buffycoat or paxgene marked as not collected
    data["recorded_buffycoat_count"] = 1
    data["recorded_paxgene_count"] = 1
    # QC report fields
    data["processed_by"] = blood_draw_crf.bscp_procby_initials
    data["protocol_deviation"] = blood_draw_crf.bscp_protocol_dev
    data["protocol_deviation_reason"] = MAPPINGS["protocol_deviation_reason"].get(
        blood_draw_crf.bscp_protocol_dev_reason, None
    )
    times = {}
    for key in [
        "bscp_aliquot_freezer_time",
        # 2021-04-19 16:58:00+01:00
        "bscp_time_blood_draw",
        # 2021-04-19 17:23:00+01:00
        "bscp_time_centrifuge",
    ]:
        times[key] = redcap_to_datetime(getattr(blood_draw_crf, key))
    data["time_to_centrifuge"] = str(
        times["bscp_time_centrifuge"] - times["bscp_time_blood_draw"]
    )
    data["time_to_freeze"] = str(
        times["bscp_aliquot_freezer_time"] - times["bscp_time_blood_draw"]
    )

    # Populate static values
    for key in ("local_id", "creation_time", "tracking_id"):
        data[key] = vbr_biosample.dict()[key]
    # Populate values derived from container
    data["case_guid"] = vbr_subject.tracking_id
    data["biosample_tracking_id"] = vbr_biosample.tracking_id
    data["visit"] = vbr_protocol.name

    # Demographic data
    demographic_crfs = vbr_api._get_rows_from_table_with_query(
        "rcap_patient_demographics_baseline_v03_demographics_i", query=query
    )
    demographic_crf = demographic_crfs[0]
    data["race"] = MAPPINGS["race"].get(demographic_crf.dem_race, "")
    data["ethnicity"] = MAPPINGS["ethnicity"].get(demographic_crf.ethnic, "")
    data["sex"] = MAPPINGS["sex"].get(demographic_crf.sex, "")
    # Deal with missing age data. Sometimes we don't have that and
    # redcap will return it as an empty string
    age = getattr(demographic_crf, "age", 0)
    if isinstance(age, str) and age == "":
        age = -1
    data["age"] = age

    return data


def build_biosample_report(biosample_id: int, vbr_api: VBR_Api) -> BiosampleReport:
    data = _build_biosample_report_data(biosample_id, vbr_api)
    return BiosampleReport(**data)


def build_biosample_report_restricted(
    biosample_id: int, vbr_api: VBR_Api
) -> BiosampleReportRestricted:
    data = _build_biosample_report_data(biosample_id, vbr_api)
    return BiosampleReportRestricted(**data)


def build_biosample_report_qc(biosample_id: int, vbr_api: VBR_Api) -> BiosampleReportQC:
    data = _build_biosample_report_data(biosample_id, vbr_api)
    return BiosampleReportQC(**data)
