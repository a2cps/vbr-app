/* comment goes here */
SELECT
    subject_base.subject_id,
    subject_base.subject_local_id,
    subject_base.subject_guid,
    subject_base.subject_project_name,
    demographics.age,
    demographics.sex,
    demographics.dem_race,
    demographics.ethnic,
    demographics.record_id
FROM
    a2cpsdev.subject_base
INNER JOIN
    a2cpsdev.rcap_patient_demographics_baseline_v03_demographics_i demographics
    ON demographics.subject_id = subject_base.subject_id;
