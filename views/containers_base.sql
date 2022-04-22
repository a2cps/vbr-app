SELECT
    container.container_id AS _container_id,
    container.local_id AS container_id,
    container.tracking_id AS container_tracking_id,
    container_type.name as container_type,
    location.display_name as location,
    status.name as status,
    ship.tracking_id,
    location.location_id as location_id
FROM a2cpsdev.container
INNER JOIN a2cpsdev.container_type
	ON container_type.container_type_id = container.container_type
INNER JOIN a2cpsdev.location
	ON location.location_id = container.location
INNER JOIN a2cpsdev.status
	ON status.status_id = container.status
LEFT JOIN a2cpsdev.container_in_shipment cont_in_ship
	ON cont_in_ship.container = container.container_id
LEFT JOIN a2cpsdev.shipment ship
	ON ship.shipment_id = cont_in_ship.shipment
	