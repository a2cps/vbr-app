SELECT
    data_event.data_event_id as _data_event_id,
    data_event.local_id as data_event_id,
    data_event.event_ts as timestamp,
    data_event.comment as comment,
    shipment.shipment_id as _shipment_id,
    shipment.local_id as shipment_id,
    shipment.tracking_id as shipment_tracking_id
FROM a2cps.data_event
LEFT JOIN a2cps.data_event_in_shipment de_in_shp
	ON data_event.data_event_id = de_in_shp.data_event
LEFT JOIN a2cps.shipment shipment
	ON shipment.shipment_id = de_in_shp.shipment
WHERE comment is not NULL and shipment_id is not NULL
ORDER BY timestamp ASC
