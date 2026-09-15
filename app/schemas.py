from datetime import datetime

from pydantic import AwareDatetime, BaseModel, ConfigDict, FiniteFloat


class TimeSeriesPoint(BaseModel):
    model_config = ConfigDict(frozen=True)

    timestamp: AwareDatetime
    value: FiniteFloat


class PerformanceSeriesInput(BaseModel):
    cost: list[TimeSeriesPoint]
    cpa: list[TimeSeriesPoint]
    roi_confirmed: list[TimeSeriesPoint]
    conversions: list[TimeSeriesPoint]


class NormalizedChartData(BaseModel):
    timestamps: list[datetime]
    cost: list[float | None]
    cpa: list[float | None]
    roi_confirmed: list[float | None]
    conversions: list[float | None]
