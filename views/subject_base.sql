SELECT
    subject.subject_id AS subject_id,
    subject.local_id AS subject_local_id,
    subject.tracking_id AS subject_guid,
    project.name AS subject_project_name
FROM
    a2cpsdev.subject
INNER JOIN
    a2cpsdev.project
    ON project.project_id = subject.project;
