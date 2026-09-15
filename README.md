# Performance time-series chart

A small FastAPI application that reproduces the provided mixed performance chart: `area`, `bar`, `spline`, and `line` series with a shared tooltip.

The backend owns the time-series contract and alignment. The browser only receives normalized data and renders it with ECharts, so the project stays Python-first and does not require a Node.js toolchain.

## Run

Python 3.12+ is required.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

Open `http://127.0.0.1:8000`. API documentation is available at `http://127.0.0.1:8000/docs`.

The chart library is loaded from jsDelivr in the browser, so the demo page needs network access on first load.

## Initialize the chart with four time-series

Each point has a timezone-aware timestamp and a numeric value. The four sequences are independent and may have different timestamps or lengths.

```python
# custom_app.py
from datetime import UTC, datetime

from app.main import create_app
from app.schemas import PerformanceSeriesInput, TimeSeriesPoint


def point(day: int, value: float) -> TimeSeriesPoint:
    return TimeSeriesPoint(
        timestamp=datetime(2026, 6, day, tzinfo=UTC),
        value=value,
    )


chart_data = PerformanceSeriesInput(
    cost=[
        point(10, 2.04),
        point(11, 25.85),
        point(12, 44.35),
        point(13, 55.65),
        point(14, 63.75),
    ],
    cpa=[
        point(10, 0.68),
        point(11, 0.86),
        point(12, 1.23),
        point(13, 0.79),
        point(14, 0.71),
    ],
    roi_confirmed=[
        point(10, 610.78),
        point(11, 180.50),
        point(12, 161.47),
        point(13, 56.33),
        point(14, 357.25),
    ],
    conversions=[
        point(10, 3),
        point(11, 30),
        point(12, 36),
        point(13, 70),
        point(14, 90),
    ],
)

app = create_app(chart_data)
```

Run the custom initialization with:

```bash
uvicorn custom_app:app --reload
```

The backend joins points by timestamp, not by list position. Missing points are returned as `null`, which leaves a gap in the corresponding line instead of pairing unrelated measurements.

Equivalent JSON can be validated and normalized with `POST /api/chart/normalize`:

```json
{
  "cost": [{"timestamp": "2026-06-12T00:00:00Z", "value": 44.35}],
  "cpa": [{"timestamp": "2026-06-12T00:00:00Z", "value": 1.23}],
  "roi_confirmed": [{"timestamp": "2026-06-12T00:00:00Z", "value": 161.47}],
  "conversions": [{"timestamp": "2026-06-12T00:00:00Z", "value": 36}]
}
```

## Data handling

- timestamps must contain a timezone;
- equal instants with different UTC offsets are aligned together;
- input order does not matter;
- missing timestamps are preserved as gaps;
- duplicate timestamps inside one series are rejected;
- non-finite numeric values are rejected by the Pydantic model.

`ROI confirmed` uses a second hidden Y axis because it has a different value range from cost, CPA, and conversions. The axes remain visually hidden to match the reference.

## Checks

```bash
ruff check .
pytest -q
```

GitHub Actions runs the same checks on every push and pull request.

## Structure

```text
app/
├── main.py                 # FastAPI app factory and endpoints
├── schemas.py              # input and normalized output contracts
├── services/
│   └── timeseries.py       # timestamp normalization and alignment
└── static/
    ├── index.html
    ├── chart.js            # ECharts configuration and tooltip behavior
    └── styles.css

tests/
├── test_api.py
└── test_timeseries.py
```
