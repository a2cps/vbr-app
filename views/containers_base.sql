SELECT
    container.container_id AS _container_id,
    container.local_id AS container_id,
    container.tracking_id AS container_tracking_id,
    container_type.name as container_type,
    location.local_id as location_id,
    location.display_name as location_display_name,
    status.name as status,
    ship.tracking_id
FROM a2cps.container
INNER JOIN a2cps.container_type
	ON container_type.container_type_id = container.container_type
INNER JOIN a2cps.location
	ON location.location_id = container.location
INNER JOIN a2cps.status
	ON status.status_id = container.status
LEFT JOIN a2cps.container_in_shipment cont_in_ship
	ON cont_in_ship.container = container.container_id
LEFT JOIN a2cps.shipment ship
	ON ship.shipment_id = cont_in_ship.shipment