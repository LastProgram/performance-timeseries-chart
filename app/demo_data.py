from datetime import datetime, timezone

from app.schemas import PerformanceSeriesInput, TimeSeriesPoint


def _point(day: int, value: float) -> TimeSeriesPoint:
    return TimeSeriesPoint(
        timestamp=datetime(2026, 6, day, tzinfo=timezone.utc),
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
        _point(10, 0.18),
        _point(11, 0.92),
        _point(12, 1.23),
        _point(13, 0.74),
        _point(14, 1.41),
    ],
    roi_confirmed=[
        _point(10, 250.0),
        _point(11, 174.0),
        _point(12, 161.47),
        _point(13, 78.0),
        _point(14, 182.0),
    ],
    conversions=[
        _point(10, 0.0),
        _point(11, 18.0),
        _point(12, 36.0),
        _point(13, 52.0),
        _point(14, 68.0),
    ],
)
