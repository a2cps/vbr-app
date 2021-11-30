from attrdict import AttrDict
from functools import lru_cache
from vbr.hashable import picklecache
from vbr.tableclasses import Table
from vbr.api import VBR_Api

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
}


@picklecache.mcache(lru_cache(maxsize=256))
def build_demographics_for_subject(subject_id: str, api: VBR_Api) -> dict:
    # rcap_patient_demographics_baseline_v03_demographics_i
    data = {"age": None, "sex": None, "race": None, "ethnicity": None}
    try:
        query = {"subject_id": {"operator": "=", "value": subject_id}}
        obj = api._get_row_from_table_with_query(
            "rcap_patient_demographics_baseline_v03_demographics_i", query=query
        )
    except ValueError:
        # No demographics available
        return data
    objd = obj.dict()
    # Direct lookup keys
    for key in ["patient_demographics_baseline_v03_demographics_i_id", "age"]:
        data[key] = objd.get(key, None)
    # Mapped keys
    data["sex"] = MAPPINGS["sex"].get(objd.get("sex"), None)
    data["race"] = MAPPINGS["race"].get(objd.get("dem_race"), None)
    data["ethnicity"] = MAPPINGS["ethnicity"].get(objd.get("ethnic"), None)
    return AttrDict(data)
