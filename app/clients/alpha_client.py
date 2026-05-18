import logging
import requests
from app.config import BASE_URL, API_KEY

logger = logging.getLogger(__name__)
base_url = BASE_URL


def get_api_key():
    api_key = API_KEY
    if not api_key:
        logger.error("ALPHA_API_KEY is missing in configuration")
        raise RuntimeError(
            "ALPHA_API_KEY is not set. Add it to a .env file or export the variable before running the app."
        )
    return api_key


def fetch_monthly_data(symbol: str):
    """Fetch monthly time series data for a symbol from Alpha Vantage."""
    params = {
        "function": "TIME_SERIES_MONTHLY",
        "symbol": symbol,
        "apikey": get_api_key()
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.error("External API request failed for %s: %s", symbol, exc)
        raise RuntimeError("Failed to fetch data from external API") from exc

    try:
        data = response.json()
    except ValueError as exc:
        logger.error("Failed to parse JSON from Alpha Vantage for %s: %s", symbol, exc)
        raise RuntimeError("Invalid response from external API") from exc

    if "Monthly Time Series" not in data:
        logger.error("Unexpected Alpha Vantage payload for %s: %s", symbol, data)
        raise RuntimeError("Invalid response from external API")

    time_series = data["Monthly Time Series"]
    parsed_data = []

    for date_str, values in time_series.items():
        year, month, _ = map(int, date_str.split("-"))
        parsed_data.append({
            "year": year,
            "month": month,
            "high": float(values["2. high"]),
            "low": float(values["3. low"]),
            "volume": int(values["5. volume"])
        })

    logger.info("Fetched %d monthly records for %s", len(parsed_data), symbol)
    return parsed_data
