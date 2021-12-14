SELECT
    data_events_public._data_event_id,
    data_events_public.data_event_id,
    data_events_public.timestamp,
    data_events_public.comment as comment,
    data_events_public.status_name,
    data_events_public.status_description,
    data_events_public.protocol_name,
    data_events_public.protocol_description,
    measurement.measurement_id as _biospecimen_id,
    measurement.local_id as biospecimen_id,
    measurement.tracking_id as biospecimen_tracking_id
FROM a2cpsdev.data_events_public
LEFT JOIN a2cpsdev.data_event_in_measurement de_in_bio
	ON data_events_public._data_event_id = de_in_bio.data_event
LEFT JOIN a2cpsdev.measurement
	ON measurement.measurement_id = de_in_bio.measurement
WHERE measurement.measurement_id is not NULL
ORDER BY timestamp ASC
