import os
import time
from datetime import datetime, timedelta
from importlib import metadata
from typing import Dict
from uuid import uuid4

from fastapi import FastAPI, Request
from pydantic import BaseModel
from starlette.responses import FileResponse

from .auditlog import logger
from .config import get_settings
from .dependencies import *
from .internal import admin, auth
from .routers import (
    biospecimens,
    container_types,
    containers,
    locations,
    organizations,
    projects,
    runlists,
    runlist_types,
    shipments,
    subjects,
    units,
)
from .utils import use_route_names_as_operation_ids
from .version import get_version

description = """
This API manages Biospecimen logistics and processing.

You are viewing the interactive documenation. Detailed reference docs are [also available](../redoc). 

"""

favicon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")

settings = get_settings()

tags_metadata = [
    {
        "name": "auth",
        "description": "Authenticate using TACC credentials.",
    },
    {
        "name": "biospecimens",
        "description": "Biospecimens are collected from Subjects.",
    },
    # {
    #     "name": "collections",
    #     "description": "Collections are virtual groupings of Biospecimens.",
    # },
    {
        "name": "containers",
        "description": "Containers hold Biospecimens.",
    },
    {
        "name": "container_types",
        "description": "Containers have a ContainerType.",
    },
    {
        "name": "locations",
        "description": "Locations hold Containers.",
    },
    {
        "name": "organizations",
        "description": "Organizations hold Locations.",
    },
    {
        "name": "projects",
        "description": "Projects are collections of Subjects.",
    },
    {
        "name": "runlists",
        "description": "RunLists are virtual collections of Biospecimens.",
    },
    {
        "name": "runlist_types",
        "description": "RunLists have a RunListType.",
    },
    {
        "name": "shipments",
        "description": "Shipments convey Containers between Locations.",
    },
    {
        "name": "subjects",
        "description": "Subjects are human participants in a Project.",
    },
    {
        "name": "units",
        "description": "Biosamples have a Unit.",
    },
    {
        "name": "admin",
        "description": "Admin endpoints manage users and roles.",
    },
    {
        "name": "status",
        "description": "Status endpoints provide basic system health checks.",
    },
]

app = FastAPI(
    title="A2CPS Virtual Biospecimen Repository API",
    description=description,
    version=get_version(),
    terms_of_service="https://portal.tacc.utexas.edu/tacc-usage-policy",
    debug=settings.app_debug,
    openapi_tags=tags_metadata,
)


@app.middleware("http")
async def add_uuid(request: Request, call_next):
    """Adds a UUID to each request."""
    request.state.uuid = uuid4().hex
    response = await call_next(request)
    response.headers["X-Request-Id"] = str(request.state.uuid)
    return response


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
        "api": app.version,
        "python_vbr": metadata.version("python_vbr"),
        "tapipy": metadata.version("tapipy"),
    }
    return v


@app.get("/", include_in_schema=False)
async def root() -> dict:
    """Returns pointers to helpful endpoints when root path is requested."""
    return {
        "application": app.title,
        "authentication": "/auth/token",
        "docs": {
            "narrative": "https://vbr-api.readthedocs.io/en/latest/",
            "interactive": "/docs",
            "detailed": "/redoc",
        },
        "status": "/status",
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


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
    dependencies=[Depends(vbr_user)],
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
app.include_router(auth.router)
app.include_router(biospecimens.router)
app.include_router(containers.router)
app.include_router(container_types.router)
app.include_router(locations.router)
app.include_router(organizations.router)
app.include_router(projects.router)
app.include_router(runlists.router)
app.include_router(runlist_types.router)
app.include_router(shipments.router)
app.include_router(subjects.router)
app.include_router(units.router)
# Admin-only routes.
# All requires VBR_ADMIN role
app.include_router(admin.router)

use_route_names_as_operation_ids(app)
