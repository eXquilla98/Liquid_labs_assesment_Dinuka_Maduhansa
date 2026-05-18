import os
import requests
from app.config import BASE_URL, API_KEY

base_url = BASE_URL


def get_api_key():
    api_key = API_KEY
    if not api_key:
        raise RuntimeError(
            "ALPHA_API_KEY is not set. Add it to a .env file or export the variable before running the app."
        )
    return api_key


def fetch_monthly_data(symbol: str):
    params = {
        "function": "TIME_SERIES_MONTHLY",
        "symbol": symbol,
        "apikey": get_api_key()
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception("Failed to fetch data from external API")

    data = response.json()

    if "Monthly Time Series" not in data:
        raise Exception("Invalid response from API")

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

    return parsed_data
