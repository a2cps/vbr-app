SELECT collection.collection_id AS _runlist_id,
    collection.local_id AS runlist_id,
    collection.tracking_id as tracking_id,
    collection.name as name,
    collection.description as description,
    collection.creation_time,
    status.name AS status_name,
    status.description AS status_description
   FROM (a2cpsdev.collection
     LEFT JOIN a2cpsdev.status ON (status.status_id = collection.status))
   WHERE collection.collection_type = 1
   ORDER BY _runlist_id ASC
