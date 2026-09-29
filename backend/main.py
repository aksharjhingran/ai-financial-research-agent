from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.services.market_data import get_stock_analysis

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
app = FastAPI(title="AI Financial Research Agent", version="0.1.0")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/", include_in_schema=False)
def index():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/stock/{ticker}")
def stock(ticker: str, period: str = Query("3mo")):
    try:
        return get_stock_analysis(ticker, period)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to retrieve market data right now.") from exc
