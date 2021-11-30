from datetime import datetime
from fastapi import FastAPI
from .config import DevelopmentConfig as Config
from .dependencies import *

from .internal import admin
from .routers import (
    biosamples,
    biosample,
    containers,
    container,
    locations,
    location,
    measurements,
    measurement,
    organizations,
    organization,
    shipments,
    shipment,
    subjects,
    subject,
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


@app.get("/status")
async def status() -> dict:
    """Provides a simple unauthenticated status check."""
    return {
        "service": app.title,
        "version": app.version,
        "tenant": Config.TAPIS_TENANT_ID,
        "status": "OK",
        "uptime": str(datetime.now() - app.state.STARTUP_TIME),
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
