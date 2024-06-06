SELECT
    DISTINCT
    sp.record_id as src_subject_id,
    TO_CHAR(TO_DATE(bsdp.bscp_time_blood_draw, 'YYYY-MM-DD'), 'MM/DD/YYYY') as interview_date,
    /* MONTHS_BETWEEN(TO_DATE(bsdp.bscp_time_blood_draw, 'YYYY-MM-DD'), TO_DATE(dem.brthdtc, 'YYYY-MM-DD'))  as interview_age, */
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
    bsdp.sex,
    bsdp.dem_race,
    bsdp.ethnic,
    surgery_type as phenotype,
    'No' as twins_study,
    'No' as sibling_study,
    'No' as family_study,
    'Yes' as sample_taken
     /* NDA_GUID as subjectkey, */
FROM a2cps.biospecimens_details_private bsdp
INNER JOIN a2cps.subjects_private sp
    ON sp.subject_id=bsdp.subject_id
INNER JOIN a2cps.rcap_patient_demographics_baseline_v03_demographics_i dem
    ON dem.record_id=sp.record_id
WHERE bsdp.protocol_name = 'baseline_visit'
