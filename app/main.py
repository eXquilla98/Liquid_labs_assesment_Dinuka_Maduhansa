import logging

from fastapi import FastAPI
from app.api.routes import router
from app.db.database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("market_data_api")

app = FastAPI()

logger.info("Initializing database and application")
init_db()

app.include_router(router)
