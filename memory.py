# memory.py
import sqlite3
from datetime import datetime

DB_NAME = "chat_history.db"

def save_summary(user_id, date, summary):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS summary (
            user_id TEXT,
            date TEXT,
            summary TEXT,
            PRIMARY KEY (user_id, date)
        )
    ''')
    cursor.execute('''
        INSERT OR REPLACE INTO summary (user_id, date, summary)
        VALUES (?, ?, ?)
    ''', (user_id, date, summary))
    conn.commit()
    conn.close()

def get_summary(user_id, date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT summary FROM summary
        WHERE user_id = ? AND date = ?
    ''', (user_id, date))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_unsummarized_dates(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 대화 저장된 날짜들
    cursor.execute('''
        SELECT DISTINCT DATE(timestamp) FROM messages
        WHERE user_id = ?
    ''', (user_id,))
    all_dates = {row[0] for row in cursor.fetchall()}

    # 요약된 날짜들
    cursor.execute('''
        SELECT date FROM summary WHERE user_id = ?
    ''', (user_id,))
    summarized = {row[0] for row in cursor.fetchall()}

    conn.close()
    return list(all_dates - summarized)
