SELECT
    data_event.data_event_id as _data_event_id,
    data_event.local_id as data_event_id,
    data_event.event_ts as timestamp,
    data_event.comment as comment,
    measurement.measurement_id as _biospecimen_id,
    measurement.local_id as biospecimen_id,
    measurement.tracking_id as biospecimen_tracking_id
FROM a2cps.data_event
LEFT JOIN a2cps.data_event_in_measurement de_in_bio
	ON data_event.data_event_id = de_in_bio.data_event
LEFT JOIN a2cps.measurement
	ON measurement.measurement_id = de_in_bio.measurement
WHERE comment is not NULL and measurement_id is not NULL
ORDER BY timestamp ASC
