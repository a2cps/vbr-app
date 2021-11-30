from typing import List, Optional

from pydantic import BaseModel, Field

from ..vbr import Measurement


class PartitionMeasurement(BaseModel):
    tracking_id: Optional[str] = Field(
        None, title="Optional tracking ID for new Measurement"
    )
    comment: Optional[str] = Field(None, title="Optional comment")


class PartitionedMeasurement(BaseModel):
    source: Measurement
    aliquot: Measurement


class ChangeMeasurementContainer(BaseModel):
    container_id: str = Field(None, title="Container Id")
    comment: Optional[str] = Field(None, title="Optional comment")


class MeasurementId(str):
    pass


class BulkChangeMeasurementContainer(BaseModel):
    container_id: str = Field(None, title="Container Id")
    measurement_ids: List[MeasurementId]
    comment: Optional[str] = Field(None, title="Optional comment")
