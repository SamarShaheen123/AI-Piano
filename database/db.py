import sqlite3
import os
from datetime import datetime

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_PATH, "database", "piano.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS practice_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            notes TEXT,
            lesson_completed INTEGER
        )
    """)

    conn.commit()
    conn.close()

def save_practice(notes, lesson_completed):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO practice_log (date, notes, lesson_completed)
        VALUES (?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        ",".join(notes),
        int(lesson_completed)
    ))

    conn.commit()
    conn.close()