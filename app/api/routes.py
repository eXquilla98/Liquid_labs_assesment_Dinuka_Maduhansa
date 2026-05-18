import logging

from fastapi import APIRouter, HTTPException
from app.models.schemas import AnnualDataResponse
from app.service.market_service import get_annual_data

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Market Data API is running.",
        "documentation": "/docs",
        "example_endpoint": "/symbols/AAPL/annual/2024"
    }


@router.get("/symbols/{symbol}/annual/{year}", response_model=AnnualDataResponse)
def get_symbol_annual(symbol: str, year: int):
    symbol = symbol.strip()

    if not symbol or len(symbol) > 10:
        logger.warning("Invalid symbol requested: %r", symbol)
        raise HTTPException(status_code=400, detail="Invalid symbol")

    if year < 1900 or year > 2100:
        logger.warning("Invalid year requested: %s", year)
        raise HTTPException(status_code=400, detail="Invalid year")

    try:
        result = get_annual_data(symbol, year)
        logger.info("Returning annual stats for %s %s", symbol, year)
        return result
    except ValueError as e:
        logger.warning("Client error for %s %s: %s", symbol, year, e)
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as exc:
        logger.error("External API failure for %s %s: %s", symbol, year, exc)
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        logger.exception(
            "Unexpected error while processing request for %s %s", symbol, year)
        raise HTTPException(status_code=500, detail="Internal server error")
