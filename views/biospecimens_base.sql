SELECT
    DISTINCT
    measurement.measurement_id AS _measurement_id,
    measurement.local_id AS biospecimen_id,
    measurement.tracking_id AS tracking_id,
    measurement.creation_time AS creation_time,
    measurement_type.name AS biospecimen_type,
    biosample.local_id AS collection_id,
    bscp.bscp_samplekit_brcd AS collection_tracking_id,
    container.local_id AS container_id,
    container.tracking_id AS container_tracking_id,
    project.name AS project,
    status_row.name AS status,
    unit.name AS unit,
    bscp.redcap_repeat_instance,
    measurement.volume,
    biosample.protocol,
    location.local_id AS collection_site_location_id,
    location.display_name AS collection_site_location_display_name
FROM
    a2cps.measurement
INNER JOIN
    a2cps.biosample
    ON biosample.biosample_id = measurement.biosample
INNER JOIN
    a2cps.location
    ON location.location_id = biosample.location
INNER JOIN
    a2cps.container
    ON container.container_id = measurement.container
INNER JOIN
    a2cps.measurement_type
    ON measurement_type.measurement_type_id = measurement.measurement_type
INNER JOIN
    a2cps.project
    ON project.project_id = measurement.project
INNER JOIN
    a2cps.status status_row
    ON status_row.status_id = measurement.status
INNER JOIN
    a2cps.unit
    ON unit.unit_id = measurement.unit
INNER JOIN
    a2cps.rcap_blood_sample_collection_and_processing_crf bscp
    ON bscp.biosample_id = measurement.biosample
        AND (bscp.redcap_repeat_instance = measurement.redcap_repeat_instance OR
            (bscp.redcap_repeat_instance is NULL AND measurement.redcap_repeat_instance is NULL))

