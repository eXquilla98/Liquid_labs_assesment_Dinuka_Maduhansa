# app/config.py

import os

API_KEY = os.getenv("ALPHA_API_KEY")

if not API_KEY:
    raise ValueError("ALPHA_API_KEY is not set")

BASE_URL = "https://www.alphavantage.co/query"
