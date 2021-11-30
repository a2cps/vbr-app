from pydantic import BaseModel, Field
from typing import Optional, List
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
    local_id: str = Field(None, title="Container Local Id")
    comment: Optional[str] = Field(None, title="Optional comment")


class MeasurementLocalId(str):
    pass


class BulkChangeMeasurementContainer(BaseModel):
    local_id: str = Field(None, title="Container Local Id")
    measurement_local_ids: List[MeasurementLocalId]
    comment: Optional[str] = Field(None, title="Optional comment")
