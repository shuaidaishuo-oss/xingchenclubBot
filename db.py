# database/db.py
import sqlite3
from datetime import datetime
from config import DB_PATH

def init_db():
    """首次运行时自动创建表格"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 记录机器人加入的所有群组和频道
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            type TEXT CHECK(type IN ('group', 'supergroup', 'channel')) NOT NULL,
            joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
            left_at TEXT
        )
    """)

    # 以后投稿、投票等表也放这里，目前先建一个示例表，防止空库报错
    cur.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    conn.commit()
    conn.close()
    print(f"数据库初始化完成：{DB_PATH}")

def add_or_update_chat(chat_id: int, title: str, chat_type: str):
    """机器人被加入新群/频道时调用"""
    conn = sqlite3.connect(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO chats (chat_id, title, type, left_at)
        VALUES (?, ?, ?, NULL)
        ON CONFLICT(chat_id) DO UPDATE SET
            title = excluded.title,
            type = excluded.type,
            left_at = NULL
    """, (chat_id, title, chat_type))
    conn.commit()
    conn.close()

def mark_chat_left(chat_id: int):
    """机器人被踢出或主动离开时调用"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        UPDATE chats SET left_at = ? WHERE chat_id = ?
    """, (datetime.utcnow().isoformat(), chat_id))
    conn.commit()
    conn.close()

# 程序启动时自动创建数据库和表格
init_db()