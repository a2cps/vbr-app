SELECT
    biosample.biosample_id AS _biosample_id,
    biosample.local_id AS collection_id,
    bscp.bscp_samplekit_brcd AS collection_tracking_id,
    biosample.creation_time AS creation_time,
    anatomy.name AS source,
    project.name AS project,
    protocol.name AS protocol,
    subject.tracking_id AS subject_guid,
    subject.local_id AS subject_id,
    bscp.bscp_aliq_cnt,
    bscp.bscp_aliquot_freezer_time,
    bscp.bscp_comments,
    bscp.bscp_deg_of_hemolysis,
    bscp.bscp_phleb_by_init,
    bscp.bscp_procby_initials,
    bscp.bscp_protocol_dev,
    bscp.bscp_time_blood_draw,
    bscp.bscp_time_centrifuge,
    bscp.redcap_repeat_instance,
    CASE 
        WHEN CAST(subject.source_subject_id AS INTEGER) BETWEEN 10000 AND 14999 THEN 'TKA'
        WHEN CAST(subject.source_subject_id AS INTEGER) BETWEEN 15000 AND 19999 THEN 'Thoracic'
        WHEN CAST(subject.source_subject_id AS INTEGER) BETWEEN 20000 AND 24999 THEN 'Thoracic'
        WHEN CAST(subject.source_subject_id AS INTEGER) BETWEEN 25000 AND 29999 THEN 'TKA'
        ELSE NULL
    END AS surgery_type
FROM
    a2cps.biosample
INNER JOIN
    a2cps.anatomy
    ON anatomy.anatomy_id = biosample.anatomy
INNER JOIN
    a2cps.project
    ON project.project_id = biosample.project
INNER JOIN
    a2cps.protocol
    ON protocol.protocol_id = biosample.protocol
INNER JOIN
    a2cps.subject
    ON subject.subject_id = biosample.subject
INNER JOIN
    a2cps.measurement
    ON measurement.biosample = biosample.biosample_id
INNER JOIN
    a2cps.rcap_blood_sample_collection_and_processing_crf bscp 
    ON bscp.biosample_id = biosample.biosample_id
        AND (bscp.redcap_repeat_instance = measurement.redcap_repeat_instance OR
            (bscp.redcap_repeat_instance is NULL AND measurement.redcap_repeat_instance is NULL))
