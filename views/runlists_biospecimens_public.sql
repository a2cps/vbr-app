SELECT
	runlists_base._collection_id as _collection_id,
	runlists_base.collection_id as runlist_id,
	runlists_base.name,
	runlists_base.description,
	measurement.local_id as biospecimen_id,
	measurement.tracking_id as biospecimen_tracking_id
FROM a2cpsdev.runlists_base
LEFT JOIN a2cpsdev.measurement_in_collection mes_in_coll
	ON runlists_base._collection_id = mes_in_coll.collection
LEFT JOIN a2cpsdev.measurement
	ON measurement.measurement_id = mes_in_coll.measurement
ORDER BY _collection_id, biospecimen_id ASC
