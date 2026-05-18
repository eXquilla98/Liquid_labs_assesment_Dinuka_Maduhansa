# Liquid Labs Market Data API Assignment

A FastAPI service that fetches monthly stock data from Alpha Vantage, caches it in SQLite, and serves annual high/low/volume stats for a given stock symbol and year.

## What this app does

- Exposes a REST API using FastAPI
- Stores data locally in SQLite without using an ORM
- Checks the local database before calling the third-party API
- Fetches monthly data from Alpha Vantage when cache is missing
- Aggregates annual values from database rows
- Returns `high`, `low`, and `volume` for the requested year and symbol

## Requirements

- Python 3.10 or later
- `pip`
- Alpha Vantage API key

## Repository structure

- `app/main.py` — FastAPI application entry point
- `app/api/routes.py` — API routes and request validation
- `app/clients/alpha_client.py` — Alpha Vantage client and data parsing
- `app/db/database.py` — SQLite connection and schema initialization
- `app/db/queries.py` — SQL queries for reading/writing cached data
- `app/service/market_service.py` — business logic for annual aggregation
- `app/models/schemas.py` — response schema definition
- `requirements.txt` — Python dependencies
- `.gitignore` — files excluded from Git

## Setup

1. Create a virtual environment:

```powershell
python -m venv .venv
```

2. Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Create `app/.env` with your Alpha Vantage API key:

```text
ALPHA_API_KEY=your_api_key_here
```

> `app/.env` is ignored by Git, so it is safe to keep your API key private.

## Run the API

```powershell
python -m uvicorn app.main:app --reload
```

Then visit:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## API Endpoint

### GET /symbols/{symbol}/annual/{year}

Returns an annual aggregation for the requested stock symbol.

Example request:

```text
GET http://127.0.0.1:8000/symbols/AAPL/annual/2024
```

Example response:

```json
{
  "high": "260.1",
  "low": "164.075",
  "volume": "14388690468"
}
```

## How it works

1. The API checks SQLite for rows matching the requested symbol and year.
2. If data exists, it aggregates and returns it.
3. If the data does not exist, it fetches monthly time series data from Alpha Vantage.
4. The fetched monthly rows are inserted into SQLite.
5. The response is built from the cached database data.

## Error handling

The app includes handling for:

- missing or invalid symbol values
- invalid year values
- missing `ALPHA_API_KEY`
- external API errors from Alpha Vantage
- no data found for the requested year

## Notes

- The database file is `market_data.db`.
- `.gitignore` excludes `.env`, virtual environments, SQLite database files, and Python cache files.
- The API is self-contained and can run locally with the command above.

## Useful URLs

- Root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI spec: `http://127.0.0.1:8000/openapi.json`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Testing examples

Use the Swagger UI or curl to test:

```powershell
curl "http://127.0.0.1:8000/symbols/AAPL/annual/2024"
```

If you want to add more examples, use other valid symbols such as `IBM`, `MSFT`, or `GOOGL`.
