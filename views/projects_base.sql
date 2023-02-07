SELECT
    project.project_id AS _project_id,
    project.local_id AS project_id,
    project.name as name,
    project.abbreviation as abbreviation,
    project.creation_time as creation_time,
    project.description as description
FROM a2cpsdev.project
