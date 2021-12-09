import time
from datetime import datetime, timedelta

from fastapi import FastAPI, Request
from pydantic import BaseModel
from importlib import metadata
from typing import Dict

from .config import get_settings
from .dependencies import *
from .internal import admin
from .routers import (
    biosample,
    biosamples,
    container,
    containers,
    location,
    locations,
    measurement,
    measurements,
    organization,
    organizations,
    shipment,
    shipments,
    subject,
    subjects,
)
from .utils import use_route_names_as_operation_ids

description = """
Virtual Biospecimen API helps manage Biospecimen logistics and processing.

"""

settings = get_settings()

tags_metadata = [
    {
        "name": "biosamples",
        "description": "Biosamples are virtual collections of Measurements.",
    },
    {
        "name": "containers",
        "description": "Containers physically hold Measurements. They can also hold other Containers.",
    },
    {"name": "locations", "description": "Containers must be in a Location."},
    {"name": "measurements", "description": "Biological samples AKA Measurements"},
    {
        "name": "organizations",
        "description": "Locations are associated with an Organization.",
    },
    {
        "name": "shipments",
        "description": "Shipments manages conveyance of Containers between Locations.",
    },
    {
        "name": "subjects",
        "description": "Human Subjects are the source of all Biosamples.",
    },
    {
        "name": "admin",
        "description": "Users and roles are managed here. The **VBR_ADMIN** role is **required**.",
    },
    {
        "name": "status",
        "description": "Provides system-level health checks.",
    },
]

app = FastAPI(
    title="Virtual Biospecimen Repository API",
    description=description,
    version="0.0.3",
    terms_of_service="https://portal.tacc.utexas.edu/tacc-usage-policy",
    contact={
        "name": "A2CPS Open Source",
        "email": "a2cps@tacc.cloud",
    },
    debug=settings.app_debug,
    openapi_tags=tags_metadata,
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Adds a timing header to each service response."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
async def startup_event():
    # Stores a timestamp so we can figure out how long the server has been up
    app.state.STARTUP_TIME = datetime.now()


class ApiStatus(BaseModel):
    """API Status Response"""

    service: str
    versions: Dict
    tenant: str
    status: str
    uptime: timedelta
    message: str


def versions():
    v = {
        "app": app.version,
        "python_vbr": metadata.version("python_vbr"),
        "tapipy": metadata.version("tapipy"),
    }
    return v


@app.get("/status", tags=["status"], response_model=ApiStatus)
async def status() -> dict:
    """Provides an unauthenticated status check."""
    return {
        "service": app.title,
        "versions": versions(),
        "tenant": settings.tapis_tenant_id,
        "status": "OK",
        "uptime": datetime.now() - app.state.STARTUP_TIME,
        "message": "Status retrieved",
    }


@app.get(
    "/status/auth",
    tags=["status"],
    dependencies=[Depends(role_vbr_user)],
    response_model=ApiStatus,
)
async def status_auth_check() -> dict:
    """Provides an authenticated status check."""
    return {
        "service": app.title,
        "versions": versions(),
        "tenant": settings.tapis_tenant_id,
        "status": "OK",
        "uptime": datetime.now() - app.state.STARTUP_TIME,
        "message": "Authentication successful",
    }


# User-mode routes
app.include_router(biosamples.router)
app.include_router(biosample.router)
app.include_router(containers.router)
app.include_router(container.router)
app.include_router(locations.router)
app.include_router(location.router)
app.include_router(measurements.router)
app.include_router(measurement.router)
app.include_router(organizations.router)
app.include_router(organization.router)
app.include_router(shipments.router)
app.include_router(shipment.router)
app.include_router(subjects.router)
app.include_router(subject.router)
# app.include_router(units.router)
# Admin-only routes.
# All requires VBR_ADMIN role
app.include_router(admin.router)

use_route_names_as_operation_ids(app)
