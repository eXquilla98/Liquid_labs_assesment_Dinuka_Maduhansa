import logging

from app.db import queries
from app.clients.alpha_client import fetch_monthly_data

logger = logging.getLogger(__name__)


def filter_by_year(api_data, year):
    return [
        item for item in api_data
        if item["year"] == year
    ]


def calculate_annual_stats(data):
    high = max(item["high"] for item in data)
    low = min(item["low"] for item in data)
    volume = sum(item["volume"] for item in data)

    return high, low, volume


def get_annual_data(symbol: str, year: int):
    """Retrieve annual stats from cache, fetch from Alpha Vantage if needed."""
    data = queries.get_monthly_data(symbol, year)

    if not data:
        logger.info("No cached data for %s %s, fetching from external API", symbol, year)
        api_data = fetch_monthly_data(symbol)
        filtered = filter_by_year(api_data, year)

        if not filtered:
            logger.warning("No monthly records found for %s %s after fetching external data", symbol, year)
            raise ValueError("No data found for the specified year")

        queries.insert_monthly_data(symbol, year, filtered)
        data = filtered
    else:
        logger.info("Using cached data for %s %s", symbol, year)

    high, low, volume = calculate_annual_stats(data)
    return {
        "high": str(high),
        "low": str(low),
        "volume": str(volume)
    }
