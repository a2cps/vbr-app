SELECT
    subject.subject_id AS _subject_id,
    subject.local_id AS subject_id,
    subject.tracking_id AS subject_guid,
    project.name AS project
FROM
    a2cpsdev.subject
INNER JOIN
    a2cpsdev.project
    ON project.project_id = subject.project;
