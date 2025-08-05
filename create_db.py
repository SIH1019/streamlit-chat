import sqlite3

conn = sqlite3.connect("chat_history.db")
cursor = conn.cursor()

# ✅ messages 테이블 생성
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# ✅ summary 테이블 생성 (지금 문제나는 부분)
cursor.execute("""
CREATE TABLE IF NOT EXISTS summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    summary TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ chat_history.db 및 모든 테이블 생성 완료!")
