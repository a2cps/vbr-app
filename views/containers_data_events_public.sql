SELECT
    data_events_public._data_event_id,
    data_events_public.data_event_id,
    data_events_public.timestamp,
    data_events_public.comment as comment,
    data_events_public.status_name,
    data_events_public.status_description,
    data_events_public.protocol_name,
    data_events_public.protocol_description,
    container.container_id as _container_id,
    container.local_id as container_id,
    container.tracking_id as container_tracking_id
FROM a2cpsdev.data_events_public
LEFT JOIN a2cpsdev.data_event_in_container de_in_con
	ON data_events_public._data_event_id = de_in_con.data_event
LEFT JOIN a2cpsdev.container container
	ON container.container_id = de_in_con.container
WHERE container_id is not NULL
ORDER BY timestamp ASC
