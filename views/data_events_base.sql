SELECT
    data_event.data_event_id as _data_event_id,
    data_event.local_id as data_event_id,
    data_event.event_ts as timestamp,
    data_event.comment as comment,
    status.name as status_name,
    status.description as status_description,
    protocol.name as protocol_name,
    protocol.description as protocol_description
FROM a2cpsdev.data_event
LEFT JOIN a2cpsdev.status
	ON status.status_id = data_event.status
LEFT JOIN a2cpsdev.protocol
	ON protocol.protocol_id = data_event.protocol
ORDER BY timestamp ASC
