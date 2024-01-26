SELECT
    DISTINCT 
    biospecimens_base._measurement_id,
    biospecimens_base.biospecimen_id,
    biospecimens_base.tracking_id,
    biospecimens_base.creation_time,
    biospecimens_base.biospecimen_type,
    biospecimens_base.collection_id,
    biospecimens_base.collection_tracking_id,
    biospecimens_base.container_id,
    biospecimens_base.container_tracking_id,
    biospecimens_base.project,
    biospecimens_base.protocol,
    biospecimens_base.status,
    biospecimens_base.unit,
    biospecimens_base.volume,
    biospecimens_base.redcap_repeat_instance,
    biospecimens_base.collection_site_location_id,
    biospecimens_base.collection_site_location_display_name,
    collections_base.subject_guid,
    collections_base.subject_id,
    collections_base.bscp_time_blood_draw,
    collections_base.bscp_time_centrifuge,
    collections_base.bscp_aliquot_freezer_time,
    collections_base.bscp_deg_of_hemolysis,
    collections_base.bscp_phleb_by_init,
    collections_base.bscp_procby_initials,
    collections_base.bscp_protocol_dev,
    collections_base.bscp_comments,
    collections_base.surgery_type,
    containers_base.location_id,
    containers_base.location_display_name,
    subjects_private.age,
    subjects_private.sex,
    subjects_private.dem_race,
    subjects_private.ethnic,
    protocol.name as protocol_name
FROM a2cpsdev.biospecimens_base
INNER JOIN a2cpsdev.collections_base
    ON biospecimens_base.collection_id = collections_base.collection_id
    AND (biospecimens_base.redcap_repeat_instance = collections_base.redcap_repeat_instance OR
            (biospecimens_base.redcap_repeat_instance is NULL AND collections_base.redcap_repeat_instance is NULL))
INNER JOIN a2cpsdev.containers_base
    ON biospecimens_base.container_id = containers_base.container_id
INNER JOIN a2cpsdev.subjects_private
    ON collections_base.subject_id = subjects_private.subject_id
INNER JOIN a2cpsdev.protocol
    ON biospecimens_base.protocol = protocol.protocol_id
