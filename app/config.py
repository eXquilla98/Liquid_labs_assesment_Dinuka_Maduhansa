import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().with_name(".env")
load_dotenv(env_path)

API_KEY = os.getenv("ALPHA_API_KEY")

if not API_KEY:
    raise ValueError("ALPHA_API_KEY is not set")

BASE_URL = "https://www.alphavantage.co/query"
