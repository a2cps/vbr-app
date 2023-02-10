SELECT
    data_events_public._data_event_id,
    data_events_public.data_event_id,
    data_events_public.timestamp,
    data_events_public.comment as comment,
    data_events_public.status_name,
    data_events_public.status_description,
    data_events_public.protocol_name,
    data_events_public.protocol_description,
    shipment.shipment_id as _shipment_id,
    shipment.local_id as shipment_id,
    shipment.tracking_id as shipment_tracking_id
FROM a2cps.data_events_public
LEFT JOIN a2cps.data_event_in_shipment de_in_shp
	ON data_events_public._data_event_id = de_in_shp.data_event
LEFT JOIN a2cps.shipment shipment
	ON shipment.shipment_id = de_in_shp.shipment
WHERE shipment_id is not NULL
ORDER BY timestamp ASC
