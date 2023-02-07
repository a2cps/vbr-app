SELECT
    data_event.data_event_id as _data_event_id,
    data_event.local_id as data_event_id,
    data_event.event_ts as timestamp,
    data_event.comment as comment
FROM a2cpsdev.data_event
	WHERE comment is not NULL
ORDER BY timestamp ASC
