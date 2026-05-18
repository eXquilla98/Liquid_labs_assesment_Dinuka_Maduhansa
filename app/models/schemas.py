from pydantic import BaseModel


class AnnualDataResponse(BaseModel):
    high: str
    low: str
    volume: str
