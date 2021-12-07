from functools import lru_cache
from typing import Union, List

from attrdict import AttrDict
from attrdict.mixins import Attr
from vbr.api import VBR_Api
from vbr.hashable import picklecache
from vbr.tableclasses import Table

from .redcap import build_demographics_for_subject

IdentOrRow = Union[Table, int]


@picklecache.mcache(lru_cache(maxsize=1024))
def _build_generic(
    entity: IdentOrRow, table_name: str, column_names: List[str], api: VBR_Api
) -> AttrDict:
    data = {}
    if entity is None:
        return None
    elif isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id(table_name, entity)
    objd = obj.dict()
    data["_{0}_id".format(table_name)] = objd.pop("{0}_id".format(table_name))
    data["{0}_id".format(table_name)] = objd.pop("local_id")
    for k in column_names:
        data[k] = objd.pop(k, None)
    # NOTE: This precludes presence of a field named "_extra" in the database response.
    data["_extra"] = objd
    return AttrDict(data)


def build_anatomy(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    return _build_generic(entity, "anatomy", ["id", "name", "description"], api)


def build_container_type(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    return _build_generic(entity, "container_type", ["name", "description"], api)


def build_measurement_type(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    return _build_generic(entity, "measurement_type", ["name", "description"], api)


def build_unit(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    return _build_generic(entity, "unit", ["name", "description"], api)


def build_organization(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    return _build_generic(entity, "organization", ["name", "description", "url"], api)


def build_project(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    return _build_generic(
        entity, "project", ["abbreviation", "name", "description"], api
    )


def build_protocol(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    return _build_generic(entity, "protocol", ["name", "description"], api)


def build_status(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    return _build_generic(entity, "status", ["name", "description"], api)


# Complex types


def build_location(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    data = _build_generic(
        entity,
        "location",
        [
            "display_name",
            "address1",
            "address2",
            "address3",
            "city",
            "state_province_country",
            "zip_or_postcode",
        ],
        api,
    )
    extra_data = data.pop("_extra", {})
    organization = extra_data.pop("organization", None)
    data["organization"] = build_organization(organization, api)
    return data


def build_container(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    data = _build_generic(
        entity,
        "container",
        [
            "tracking_id",
        ],
        api,
    )
    extra_data = data.pop("_extra", {})
    location = extra_data.pop("location", None)
    data["location"] = build_location(location, api)
    status = extra_data.pop("status", None)
    data["status"] = build_status(status, api)
    container_type = extra_data.pop("container_type", None)
    data["container_type"] = build_container_type(container_type, api)
    return data


def build_shipment(entity: IdentOrRow, api: VBR_Api) -> AttrDict:
    data = _build_generic(
        entity,
        "shipment",
        ["name", "sender_name", "tracking_id"],
        api,
    )
    extra_data = data.pop("_extra", {})
    ship_from = extra_data.pop("ship_from", None)
    data["ship_from"] = build_location(ship_from, api)
    ship_to = extra_data.pop("ship_to", None)
    data["ship_to"] = build_location(ship_to, api)
    project = extra_data.pop("project", None)
    data["project"] = build_project(project, api)
    status = extra_data.pop("status", None)
    data["status"] = build_status(status, api)
    return data


@picklecache.mcache(lru_cache(maxsize=256))
def build_data_event(entity: IdentOrRow, api: VBR_Api) -> dict:
    data = {}
    if isinstance(entity, Table):
        obj = entity
    else:
        obj = api._get_row_from_table_with_id("data_event", entity)
    objd = obj.dict()
    data["_data_event_id"] = objd["data_event_id"]
    data["data_event_id"] = objd["local_id"]
    for key in ("comment", "event_ts", "rank"):
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
    data["_subject_id"] = objd["subject_id"]
    data["subject_id"] = objd["local_id"]
    for key in (
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
        data["_subject_id"], api
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
    data["_biosample_id"] = objd["biosample_id"]
    data["biosample_id"] = objd["local_id"]
    for key in ("creation_time", "tracking_id"):
        data[key] = objd.get(key, None)
    # Nested values
    data["anatomy"] = build_anatomy(objd.get("anatomy", None), api)
    data["project"] = build_project(objd.get("project", None), api)
    data["protocol"] = build_protocol(objd.get("protocol", None), api)
    data["subject"] = build_subject(objd.get("subject", None), api)
    # TODO: add "redcap" dict
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
    data["_measurement_id"] = objd["measurement_id"]
    data["measurement_id"] = objd["local_id"]
    for key in ("creation_time", "tracking_id"):
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
