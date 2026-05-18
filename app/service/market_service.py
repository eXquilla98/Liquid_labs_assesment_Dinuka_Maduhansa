from app.db import queries
from app.clients.alpha_client import fetch_monthly_data


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

    data = queries.get_monthly_data(symbol, year)

    if not data:

        api_data = fetch_monthly_data(symbol)
        filtered = filter_by_year(api_data, year)

        if not filtered:
            raise ValueError("No data found for the specified year")

        queries.insert_monthly_data(symbol, year, filtered)
        data = filtered

    high, low, volume = calculate_annual_stats(data)

    return {
        "high": str(high),
        "low": str(low),
        "volume": str(volume)
    }
