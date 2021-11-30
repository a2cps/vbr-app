from datetime import datetime, timedelta

from fastapi import FastAPI
from pydantic import BaseModel

from .config import DevelopmentConfig as Config
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

description = """
Virtual Biospecimen API helps manage Biospecimen logistics and processing.

"""

app = FastAPI(
    title="Virtual Biospecimen Repository API",
    description=description,
    version="0.0.2",
    terms_of_service="https://portal.tacc.utexas.edu/tacc-usage-policy",
    contact={
        "name": "A2CPS Open Source",
        "email": "a2cps@tacc.cloud",
    },
    debug=Config.DEBUG,
)


@app.on_event("startup")
async def startup_event():
    app.state.STARTUP_TIME = datetime.now()


class ApiStatus(BaseModel):
    service: str
    version: str
    tenant: str
    status: str
    uptime: timedelta
    message: str


@app.get("/status", response_model=ApiStatus)
async def status() -> dict:
    """Provides an unauthenticated status check."""
    return {
        "service": app.title,
        "version": app.version,
        "tenant": Config.TAPIS_TENANT_ID,
        "status": "OK",
        "uptime": datetime.now() - app.state.STARTUP_TIME,
        "message": "Status retrieved",
    }


@app.get(
    "/status/auth", dependencies=[Depends(role_vbr_user)], response_model=ApiStatus
)
async def status_auth_check() -> dict:
    """Provides an authenticated status check."""
    return {
        "service": app.title,
        "version": app.version,
        "tenant": Config.TAPIS_TENANT_ID,
        "status": "OK",
        "uptime": datetime.now() - app.state.STARTUP_TIME,
        "message": "Authenication successful",
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
