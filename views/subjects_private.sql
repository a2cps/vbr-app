/* comment goes here */
SELECT
    subjects_base._subject_id,
    subjects_base.subject_id,
    subjects_base.subject_guid,
    subjects_base.project,
    demographics.age,
    demographics.sex,
    demographics.dem_race,
    demographics.ethnic,
    demographics.record_id
FROM
    a2cpsdev.subjects_base
INNER JOIN
    a2cpsdev.rcap_patient_demographics_baseline_v03_demographics_i demographics
    ON demographics.subject_id = subjects_base._subject_id;
