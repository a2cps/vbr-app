SELECT
    location.location_id AS _location_id,
    location.local_id AS location_id,
    location.display_name as display_name,
    location.address1 as address1,
    location.address2 as address2,
    location.address3 as address3,
    location.city as city,
    location.state_province_country as state_province_country,
    location.zip_or_postcode as zip_or_postcode,
    organization.name as organization
FROM a2cps.location
INNER JOIN
    a2cps.organization
    ON organization.organization_id = location.organization
