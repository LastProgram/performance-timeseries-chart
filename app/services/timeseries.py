from collections.abc import Iterable
from datetime import UTC, datetime

from app.schemas import NormalizedChartData, PerformanceSeriesInput, TimeSeriesPoint

SERIES_NAMES = ("cost", "cpa", "roi_confirmed", "conversions")


class DuplicateTimestampError(ValueError):
    pass


def normalize_series(data: PerformanceSeriesInput) -> NormalizedChartData:
    indexes = {
        name: _index_series(getattr(data, name), series_name=name) for name in SERIES_NAMES
    }
    timestamps = sorted({timestamp for index in indexes.values() for timestamp in index})

    return NormalizedChartData(
        timestamps=timestamps,
        **{
            name: [indexes[name].get(timestamp) for timestamp in timestamps]
            for name in SERIES_NAMES
        },
    )


def _index_series(
    points: Iterable[TimeSeriesPoint],
    *,
    series_name: str,
) -> dict[datetime, float]:
    result: dict[datetime, float] = {}

    for point in points:
        # Независимые серии связываются по моменту времени, а не по позиции элемента.
        timestamp = point.timestamp.astimezone(UTC)
        if timestamp in result:
            raise DuplicateTimestampError(
                f"Series '{series_name}' contains duplicate timestamp {timestamp.isoformat()}"
            )
        result[timestamp] = float(point.value)

    return result
