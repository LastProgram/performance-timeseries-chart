from datetime import UTC, datetime, timedelta, timezone

import pytest

from app.schemas import PerformanceSeriesInput, TimeSeriesPoint
from app.services.timeseries import DuplicateTimestampError, normalize_series


def point(day: int, value: float, *, tz: timezone = UTC) -> TimeSeriesPoint:
    return TimeSeriesPoint(timestamp=datetime(2026, 6, day, tzinfo=tz), value=value)


def test_normalize_series_sorts_and_aligns_independent_sequences() -> None:
    data = PerformanceSeriesInput(
        cost=[point(12, 44.36), point(10, 10.0)],
        cpa=[point(10, 1.0)],
        roi_confirmed=[point(11, 150.0)],
        conversions=[point(12, 36.0)],
    )

    result = normalize_series(data)

    assert [timestamp.day for timestamp in result.timestamps] == [10, 11, 12]
    assert result.cost == [10.0, None, 44.36]
    assert result.cpa == [1.0, None, None]
    assert result.roi_confirmed == [None, 150.0, None]
    assert result.conversions == [None, None, 36.0]


def test_normalize_series_matches_equal_instants_with_different_offsets() -> None:
    plus_two = timezone(timedelta(hours=2))
    data = PerformanceSeriesInput(
        cost=[TimeSeriesPoint(timestamp=datetime(2026, 6, 12, 10, tzinfo=plus_two), value=44.36)],
        cpa=[TimeSeriesPoint(timestamp=datetime(2026, 6, 12, 8, tzinfo=UTC), value=1.23)],
        roi_confirmed=[],
        conversions=[],
    )

    result = normalize_series(data)

    assert len(result.timestamps) == 1
    assert result.timestamps[0] == datetime(2026, 6, 12, 8, tzinfo=UTC)
    assert result.cost == [44.36]
    assert result.cpa == [1.23]


def test_normalize_series_rejects_duplicate_timestamp() -> None:
    data = PerformanceSeriesInput(
        cost=[point(12, 10.0), point(12, 20.0)],
        cpa=[],
        roi_confirmed=[],
        conversions=[],
    )

    with pytest.raises(DuplicateTimestampError, match="cost"):
        normalize_series(data)
