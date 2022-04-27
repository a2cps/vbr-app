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
    biospecimens_base.status,
    biospecimens_base.unit,
    biospecimens_base.volume,
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
    containers_base.location_id,
    containers_base.location_display_name
FROM a2cpsdev.biospecimens_base
INNER JOIN a2cpsdev.collections_base
    ON biospecimens_base.collection_id = collections_base.collection_id
INNER JOIN a2cpsdev.containers_base
    ON biospecimens_base.container_id = containers_base.container_id
