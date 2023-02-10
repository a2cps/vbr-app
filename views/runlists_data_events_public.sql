SELECT
    data_events_public._data_event_id,
    data_events_public.data_event_id,
    data_events_public.timestamp,
    data_events_public.comment as comment,
    data_events_public.status_name,
    data_events_public.status_description,
    data_events_public.protocol_name,
    data_events_public.protocol_description,
    collection.collection_id as _collection_id,
    collection.local_id as collection_id,
    collection.tracking_id as collection_tracking_id
FROM a2cps.data_events_public
LEFT JOIN a2cps.data_event_in_collection de_in_shp
	ON data_events_public._data_event_id = de_in_shp.data_event
LEFT JOIN a2cps.collection collection
	ON collection.collection_id = de_in_shp.collection
WHERE collection_id is not NULL
ORDER BY timestamp ASC
