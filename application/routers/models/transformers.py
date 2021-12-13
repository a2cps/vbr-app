from typing import Dict, List

__all__ = ["transform"]


def transform_redcap(data: Dict) -> Dict:
    # (source_key, destination_key, {value:mapping})
    MAPPINGS = [
        ("sex", "sex", {1: "Male", 2: "Female", 3: "Unknown", 4: "Intersex"}),
        (
            "dem_race",
            "race",
            {
                1: "American Indian or Alaska Native",
                2: "Asian",
                3: "Black or African-American",
                4: "Native Hawaiian or Pacific Islander",
                5: "White",
                6: "Unknown",
                7: "Not Reported",
            },
        ),
        (
            "ethnic",
            "ethnicity",
            {
                1: "Hispanic or Latino",
                2: "Not Hispanic or Latino",
                3: "Unknown",
                4: "Not reported",
            },
        ),
    ]

    for source, destination, valuemap in MAPPINGS:
        value = data.pop(source, None)
        if value is not None:
            data[destination] = valuemap.get(value, None)
    return data


def transform(data: Dict) -> Dict:
    data = transform_redcap(data)
    return data
