import sqlite3

# 대화 저장
def save_message(user_id, role, message):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (user_id, role, message) VALUES (?, ?, ?)", (user_id, role, message))
    conn.commit()
    conn.close()

# 대화 불러오기 (최신 10개만)
def get_chat_history(user_id, limit=10):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, message FROM messages 
        WHERE user_id = ? 
        ORDER BY timestamp DESC LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": role, "content": msg} for role, msg in reversed(rows)]

# 날짜별 대화 불러오기
def get_chat_history_by_date(user_id, date):
    conn = sqlite3.connect("chat_history.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT role, message, timestamp FROM messages
        WHERE user_id = ? AND DATE(timestamp) = ?
        ORDER BY timestamp ASC
    ''', (user_id, date))
    rows = cursor.fetchall()
    conn.close()
    return rows
