SELECT
    DISTINCT
    measurement.measurement_id AS _measurement_id,
    measurement.local_id AS biospecimen_id,
    measurement.tracking_id AS tracking_id,
    measurement.creation_time AS creation_time,
    measurement_type.name AS biospecimen_type,
    biosample.local_id AS collection_id,
    biosample.tracking_id AS collection_tracking_id,
    container.local_id AS container_id,
    container.tracking_id AS container_tracking_id,
    project.name AS project,
    status_row.name AS status,
    unit.name AS unit,
    measurement.volume
FROM
    a2cpsdev.measurement
INNER JOIN
    a2cpsdev.biosample
    ON biosample.biosample_id = measurement.biosample
INNER JOIN
    a2cpsdev.container
    ON container.container_id = measurement.container
INNER JOIN
    a2cpsdev.measurement_type
    ON measurement_type.measurement_type_id = measurement.measurement_type
INNER JOIN
    a2cpsdev.project
    ON project.project_id = measurement.project
INNER JOIN
    a2cpsdev.status status_row
    ON status_row.status_id = measurement.status
INNER JOIN
    a2cpsdev.unit
    ON unit.unit_id = measurement.unit
