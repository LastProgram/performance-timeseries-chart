from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.demo_data import DEMO_DATA
from app.schemas import NormalizedChartData, PerformanceSeriesInput
from app.services.timeseries import DuplicateTimestampError, normalize_series

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Performance time-series chart",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/chart/demo", response_model=NormalizedChartData)
def get_demo_chart() -> NormalizedChartData:
    return normalize_series(DEMO_DATA)


@app.post("/api/chart", response_model=NormalizedChartData)
def prepare_chart(data: PerformanceSeriesInput) -> NormalizedChartData:
    try:
        return normalize_series(data)
    except DuplicateTimestampError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
