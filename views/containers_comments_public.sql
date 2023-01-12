SELECT
    data_event.data_event_id as _data_event_id,
    data_event.local_id as data_event_id,
    data_event.event_ts as timestamp,
    data_event.comment as comment,
    container.container_id as _container_id,
    container.local_id as container_id,
    container.tracking_id as container_tracking_id
FROM a2cps.data_event
LEFT JOIN a2cps.data_event_in_container de_in_con
	ON data_event.data_event_id = de_in_con.data_event
LEFT JOIN a2cps.container container
	ON container.container_id = de_in_con.container
WHERE comment is not NULL and container_id is not NULL
ORDER BY timestamp ASC
