SELECT collection.collection_id AS _runlist_id,
    collection.local_id AS runlist_id,
    collection.tracking_id as tracking_id,
    collection.name as name,
    collection.description as description,
    collection.creation_time,
    status.name AS status_name,
    status.description AS status_description,
    collection_type.name as type,
    location.local_id as location_id,
    location.display_name as location_display_name
   FROM (a2cpsdev.collection
     LEFT JOIN a2cpsdev.status ON (status.status_id = collection.status)
     LEFT JOIN a2cpsdev.collection_type ON (collection_type.collection_type_id = collection.collection_type)
     LEFT JOIN a2cpsdev.location ON (location.location_id = collection.location))
   WHERE collection.collection_type >= 1
   ORDER BY _runlist_id ASC
