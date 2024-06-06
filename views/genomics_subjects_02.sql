SELECT
    DISTINCT
    dem.record_id as src_subject_id,
    TO_CHAR(TO_DATE(bsdp.bscp_time_blood_draw, 'YYYY-MM-DD'), 'MM/DD/YYYY') as interview_date,
    ROUND( 
        EXTRACT(year FROM age(
            TO_DATE(bsdp.bscp_time_blood_draw, 'YYYY-MM-DD'),
            TO_DATE(dem.brthdtc, 'YYYY-MM-DD')
        ))*12 + 
        EXTRACT(month FROM age(
            TO_DATE(bsdp.bscp_time_blood_draw, 'YYYY-MM-DD'),
            TO_DATE(dem.brthdtc, 'YYYY-MM-DD')
            )) +
        EXTRACT(day FROM age(
            TO_DATE(bsdp.bscp_time_blood_draw, 'YYYY-MM-DD'),
            TO_DATE(dem.brthdtc, 'YYYY-MM-DD')
            ))/30.437
     )::INTEGER as interview_age,
    dem.sex,
    dem.dem_race,
    dem.ethnic,
    CASE 
        WHEN CAST(dem.record_id AS INTEGER) BETWEEN 10000 AND 14999 THEN 'TKA'
        WHEN CAST(dem.record_id AS INTEGER) BETWEEN 15000 AND 19999 THEN 'Thoracic'
        WHEN CAST(dem.record_id AS INTEGER) BETWEEN 20000 AND 24999 THEN 'Thoracic'
        WHEN CAST(dem.record_id AS INTEGER) BETWEEN 25000 AND 29999 THEN 'TKA'
        ELSE NULL
    END AS  phenotype,
    'No' as twins_study,
    'No' as sibling_study,
    'No' as family_study,
    CASE 
        WHEN bsdp.biospecimen_id IS NOT NULL
        THEN 'Yes'
        ELSE 'No' END AS sample_taken
     /* NDA_GUID as subjectkey, */
FROM  a2cps.rcap_patient_demographics_baseline_v03_demographics_i dem
LEFT JOIN a2cps.subjects_private sp
    ON dem.record_id=sp.record_id
LEFT JOIN a2cps.biospecimens_details_private bsdp
    ON sp.subject_id=bsdp.subject_id  AND bsdp.protocol_name = 'baseline_visit'
WHERE bsdp.protocol_name = 'baseline_visit' OR bsdp.protocol_name IS NULL

