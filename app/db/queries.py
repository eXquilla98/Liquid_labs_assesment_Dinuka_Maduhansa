from app.db.database import get_db_connection


def insert_monthly_data(symbol, year, data):
    conn = get_db_connection()
    cursor = conn.cursor()

    for item in data:
        try:
            cursor.execute('''                              
                INSERT INTO monthly_data (symbol, year, month, high, low, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                year,
                item["month"],
                item["high"],
                item["low"],
                item["volume"]))
        except Exception as e:
            print(f"Error inserting data: {e}")

    conn.commit()
    conn.close()
