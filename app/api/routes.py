from fastapi import APIRouter, HTTPException
from app.models.schemas import AnnualDataResponse
from app.service.market_service import get_annual_data

router = APIRouter()


@router.get("/symbols/{symbol}/annual/{year}", response_model=AnnualDataResponse)
def get_symbol_annual(symbol: str, year: int):
    if len(symbol) > 10:
        raise HTTPException(status_code=400, detail="Invalid symbol")

    if year < 1900 or year > 2100:
        raise HTTPException(status_code=400, detail="Invalid year")
    try:
        result = get_annual_data(symbol, year)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
