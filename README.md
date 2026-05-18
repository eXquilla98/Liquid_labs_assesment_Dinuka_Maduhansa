# Liquid Labs Market Data API Assignment

A simple FastAPI service that fetches monthly stock prices from Alpha Vantage, stores the data in an SQLite database, and returns annual high/low/volume values for a given symbol and year.

## Requirements

- Python 3.10+
- `pip`
- Alpha Vantage API key

## Setup

1. Create a virtual environment:

```powershell
python -m venv .venv
```

2. Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Add your API key to `app/.env`:

```text
ALPHA_API_KEY=your_api_key_here
```

> Do not commit this file. It is ignored by Git.

## Running the API

```powershell
python -m uvicorn app.main:app --reload
```

Then open:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Endpoint

- `GET /symbols/{symbol}/annual/{year}`

Example:

```text
GET /symbols/AAPL/annual/2024
```

Response:

```json
{
  "high": "...",
  "low": "...",
  "volume": "..."
}
```

## Notes

- The API checks the local SQLite database first.
- If the requested symbol and year are not cached, it fetches monthly data from Alpha Vantage, stores it locally, and then returns the aggregated result.
- The database file is stored as `market_data.db` and is ignored by Git.
