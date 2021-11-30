from typing import Union
from attrdict import AttrDict
from functools import lru_cache
from vbr.hashable import picklecache
from vbr.tableclasses import Table
from vbr.api import VBR_Api
from .redcap import build_demographics_for_subject


# TODO - make each builder accept either Table instance or entity.
IdentOrRow = Union[Table, int]


@picklecache.mcache(lru_cache(maxsize=256))
def build_anatomy(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("anatomy", entity)
    for key in ("anatomy_id", "id", "name", "description"):
        data[key] = obj.dict().get(key, None)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_location(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("location", entity)
    for key in (
        "location_id",
        "local_id",
        "display_name",
        "address1",
        "address2",
        "address3",
        "city",
        "state_province_country",
        "zip_or_postcode",
    ):
        data[key] = obj.dict().get(key, None)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_container_type(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("container_type", entity)
    for key in ("container_type_id", "name", "description"):
        data[key] = obj.dict().get(key, None)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_measurement_type(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("measurement_type", entity)
    for key in ("measurement_type_id", "name", "description"):
        data[key] = obj.dict().get(key, None)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_unit(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("unit", entity)
    for key in ("unit_id", "name", "description"):
        data[key] = obj.dict().get(key, None)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_organization(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("organization", entity)
    for key in ("organization_id", "name", "description", "url"):
        data[key] = obj.dict().get(key, None)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_project(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("project", entity)
    for key in ("project_id", "abbreviation", "name", "description"):
        data[key] = obj.dict().get(key, None)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_protocol(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("protocol", entity)
    for key in ("protocol_id", "name", "description"):
        data[key] = obj.dict().get(key, None)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_status(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("status", entity)
    for key in ("status_id", "name", "description"):
        data[key] = obj.dict().get(key, None)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_data_event(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("data_event", entity)
    objd = obj.dict()
    for key in ("data_event_id", "local_id", "comment", "event_ts", "rank"):
        data[key] = objd.get(key, None)
    try:
        data["protocol"] = build_protocol(objd.get("protocol", None), api)
    except Exception:
        data["protocol"] = None
    try:
        data["status"] = build_status(objd.get("status", None), api)
    except Exception:
        data["status"] = None
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_subject(entity: IdentOrRow, api: VBR_Api, restricted: bool = True) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("subject", entity)
    objd = obj.dict()
    for key in (
        "subject_id",
        "local_id",
        "creation_time",
        "tracking_id",
        "granularity",
        "source_subject_id",  # Make sure this remains restricted
    ):
        data[key] = objd.get(key, None)
    # Nested values
    data["project"] = build_project(objd.get("project", None), api)
    # These will be populated from redcap forms, keyed on form name
    # Format: restricted["formname"][{data}]
    # For cases where there is one instance of a form
    # we will simply use item "0"
    data["restricted"] = {}
    data["restricted"]["demographics"] = build_demographics_for_subject(
        data["subject_id"], api
    )
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_biosample(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api.get_biosample(entity)
    objd = obj.dict()
    for key in ("biosample_id", "creation_time", "local_id", "tracking_id"):
        data[key] = objd.get(key, None)
    # Nested values
    data["anatomy"] = build_anatomy(objd.get("anatomy", None), api)
    data["project"] = build_project(objd.get("project", None), api)
    data["protocol"] = build_protocol(objd.get("protocol", None), api)
    data["subject"] = build_subject(objd.get("subject", None), api)
    # TODO: add "redcap" dict
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_container(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api.get_container(entity)
    objd = obj.dict()
    # Start with static values
    for key in ("container_id", "local_id", "tracking_id"):
        data[key] = objd.get(key, None)
    # Nested values
    data["container_type"] = build_container_type(objd.get("container_type", None), api)
    data["location"] = build_location(objd.get("location", None), api)
    data["status"] = build_status(objd.get("status", None), api)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_measurement(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api.get_measurement(entity)
    objd = obj.dict()
    # Start with static values
    for key in ("measurement_id", "creation_time", "local_id", "tracking_id"):
        data[key] = objd.get(key, None)
    # Nested values
    data["biosample"] = build_biosample(objd.get("biosample", None), api)
    data["container"] = build_container(objd.get("container", None), api)
    data["biosample"] = build_biosample(objd.get("biosample", None), api)
    data["project"] = build_project(objd.get("project", None), api)
    data["measurement_type"] = build_measurement_type(
        objd.get("measurement_type", None), api
    )
    data["status"] = build_status(objd.get("status", None), api)
    data["unit"] = build_unit(objd.get("unit", None), api)
    return AttrDict(data)


@picklecache.mcache(lru_cache(maxsize=256))
def build_shipment(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api.get_shipment(entity)
    objd = obj.dict()
    # Start with static values
    for key in ("shipment_id", "local_id", "name", "sender_name", "tracking_id"):
        data[key] = objd.get(key, None)
    # Nested values
    data["ship_from"] = build_location(objd.get("ship_from", None), api)
    data["ship_to"] = build_location(objd.get("ship_to", None), api)
    data["project"] = build_project(objd.get("project", None), api)
    data["status"] = build_status(objd.get("status", None), api)
    return AttrDict(data)
