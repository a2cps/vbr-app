SELECT
    collection_type.collection_type_id AS _runlist_type_id,
    collection_type.local_id AS runlist_type_id,
    collection_type.name as name,
    collection_type.description as description
FROM a2cpsdev.collection_type
