import logging
from app.db.database import get_db_connection

logger = logging.getLogger(__name__)


def get_monthly_data(symbol, year):
    """Return cached monthly rows for a symbol and year from SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT month, high, low, volume FROM monthly_data WHERE symbol = ? AND year = ? ORDER BY month",
        (symbol, year)
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        logger.info("Cache miss for symbol=%s year=%s", symbol, year)
        return []

    logger.info("Cache hit for symbol=%s year=%s, rows=%d", symbol, year, len(rows))
    return [
        {
            "month": row[0],
            "high": row[1],
            "low": row[2],
            "volume": row[3]
        }
        for row in rows
    ]


def insert_monthly_data(symbol, year, data):
    conn = get_db_connection()
    cursor = conn.cursor()

    for item in data:
        try:
            cursor.execute(
                '''
                INSERT INTO monthly_data (symbol, year, month, high, low, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                year,
                item["month"],
                item["high"],
                item["low"],
                item["volume"]
            ))
        except Exception as exc:
            logger.error("Error inserting data for %s %s: %s", symbol, year, exc)

    conn.commit()
    conn.close()
    logger.info("Inserted %d monthly rows for %s %s", len(data), symbol, year)
