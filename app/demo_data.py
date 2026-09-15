from datetime import UTC, datetime

from app.schemas import PerformanceSeriesInput, TimeSeriesPoint


def _point(day: int, value: float) -> TimeSeriesPoint:
    return TimeSeriesPoint(
        timestamp=datetime(2026, 6, day, tzinfo=UTC),
        value=value,
    )


DEMO_DATA = PerformanceSeriesInput(
    cost=[
        _point(10, 0.0),
        _point(11, 20.1),
        _point(12, 44.36),
        _point(13, 56.8),
        _point(14, 69.5),
    ],
    cpa=[
        _point(10, 0.82),
        _point(11, 1.04),
        _point(12, 1.23),
        _point(13, 0.91),
        _point(14, 1.37),
    ],
    roi_confirmed=[
        _point(10, 620.0),
        _point(11, 180.0),
        _point(12, 161.47),
        _point(13, 50.0),
        _point(14, 360.0),
    ],
    conversions=[
        _point(10, 0.0),
        _point(11, 19.0),
        _point(12, 36.0),
        _point(13, 48.0),
        _point(14, 61.0),
    ],
)
