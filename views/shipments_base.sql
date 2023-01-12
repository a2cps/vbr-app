SELECT
    shipment.shipment_id AS _shipment_id,
    shipment.local_id AS shipment_id,
    shipment.tracking_id AS tracking_id,
    shipment.name AS shipment_name,
    shipment.sender_name AS sender_name,
    project.name AS project_name,
    ship_from.display_name AS ship_from,
    ship_to.display_name AS ship_to,
    status_row.name AS status
FROM
    a2cps.shipment
INNER JOIN
    a2cps.project
    ON project.project_id = shipment.project
INNER JOIN
    a2cps.location ship_from
    ON ship_from.location_id = shipment.ship_from
INNER JOIN
    a2cps.location ship_to
    ON ship_to.location_id = shipment.ship_to
INNER JOIN
    a2cps.status status_row
    ON status_row.status_id = shipment.status
