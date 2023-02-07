SELECT
    data_event.data_event_id as _data_event_id,
    data_event.local_id as data_event_id,
    data_event.event_ts as timestamp,
    data_event.comment as comment,
    collection.collection_id as _collection_id,
    collection.local_id as collection_id,
    collection.tracking_id as collection_tracking_id
FROM a2cpsdev.data_event
LEFT JOIN a2cpsdev.data_event_in_collection de_in_shp
	ON data_event.data_event_id = de_in_shp.data_event
LEFT JOIN a2cpsdev.collection collection
	ON collection.collection_id = de_in_shp.collection
WHERE comment is not NULL and collection_id is not NULL
ORDER BY timestamp ASC
