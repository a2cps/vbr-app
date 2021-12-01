import re
from fastapi import FastAPI
from fastapi.routing import APIRoute


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


def recognize_delivery_service(tracking_code: str):
    """Infer the carrier for a tracking code.

    Can be used as a quick validation."""

    service = None

    # Strip whitespace
    tracking_code = re.sub(r"\s+", "", tracking_code)

    usps_pattern = [
        "^(94|93|92|94|95)[0-9]{20}$",
        "^(94|93|92|94|95)[0-9]{22}$",
        "^(70|14|23|03)[0-9]{14}$",
        "^(M0|82)[0-9]{8}$",
        "^([A-Z]{2})[0-9]{9}([A-Z]{2})$",
    ]

    ups_pattern = [
        "^(1Z)[0-9A-Z]{16}$",
        "^(T)+[0-9A-Z]{10}$",
        "^[0-9]{9}$",
        "^[0-9]{26}$",
    ]

    fedex_pattern = ["^[0-9]{20}$", "^[0-9]{15}$", "^[0-9]{12}$", "^[0-9]{22}$"]

    usps = "(" + ")|(".join(usps_pattern) + ")"
    fedex = "(" + ")|(".join(fedex_pattern) + ")"
    ups = "(" + ")|(".join(ups_pattern) + ")"

    if re.match(usps, tracking_code) != None:
        service = "USPS"
    elif re.match(ups, tracking_code) != None:
        service = "UPS"
    elif re.match(fedex, tracking_code) != None:
        service = "FedEx"
    else:
        raise ValueError("Unable to determine service for %s", tracking_code)

    return service
