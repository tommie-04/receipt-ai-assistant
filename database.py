import sqlite3
from datetime import datetime
import json

DB_NAME = "receipts.db"

def init_db():
    """Create the transactions table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            merchant TEXT,
            total TEXT,
            date TEXT,
            category TEXT,
            items_json TEXT,
            uploaded_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_transaction(username, merchant, total, date, category, items):
    """Save a single transaction to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (username, merchant, total, date, category, items_json, uploaded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        merchant,
        total,
        date,
        category,
        json.dumps(items),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_user_transactions(username):
    """Retrieve all transactions for a given user, most recent first."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT merchant, total, date, category, items_json, uploaded_at
        FROM transactions
        WHERE username = ?
        ORDER BY uploaded_at DESC
    """, (username,))
    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        results.append({
            "merchant": row[0],
            "total": row[1],
            "date": row[2],
            "category": row[3],
            "items": json.loads(row[4]) if row[4] else [],
            "uploaded_at": row[5]
        })
    return results