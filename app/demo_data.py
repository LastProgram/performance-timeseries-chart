from datetime import UTC, datetime

from app.schemas import PerformanceSeriesInput, TimeSeriesPoint


def _point(day: int, value: float) -> TimeSeriesPoint:
    return TimeSeriesPoint(
        timestamp=datetime(2026, 6, day, tzinfo=UTC),
        value=value,
    )


DEMO_DATA = PerformanceSeriesInput(
    cost=[
        _point(10, 2.04),
        _point(11, 25.85),
        _point(12, 44.35),
        _point(13, 55.65),
        _point(14, 63.75),
    ],
    cpa=[
        _point(10, 0.68),
        _point(11, 0.86),
        _point(12, 1.23),
        _point(13, 0.79),
        _point(14, 0.71),
    ],
    roi_confirmed=[
        _point(10, 610.78),
        _point(11, 180.50),
        _point(12, 161.47),
        _point(13, 56.33),
        _point(14, 357.25),
    ],
    conversions=[
        _point(10, 3),
        _point(11, 30),
        _point(12, 36),
        _point(13, 70),
        _point(14, 90),
    ],
)
