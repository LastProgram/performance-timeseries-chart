from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.demo_data import DEMO_DATA
from app.schemas import NormalizedChartData, PerformanceSeriesInput
from app.services.timeseries import DuplicateTimestampError, normalize_series

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


def create_app(chart_data: PerformanceSeriesInput | None = None) -> FastAPI:
    initial_data = chart_data or DEMO_DATA
    api = FastAPI(
        title="Performance time-series chart",
        version="0.1.0",
    )
    api.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @api.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @api.get("/api/chart", response_model=NormalizedChartData)
    def get_chart() -> NormalizedChartData:
        return normalize_series(initial_data)

    @api.post("/api/chart/normalize", response_model=NormalizedChartData)
    def prepare_chart(data: PerformanceSeriesInput) -> NormalizedChartData:
        try:
            return normalize_series(data)
        except DuplicateTimestampError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return api


app = create_app()
