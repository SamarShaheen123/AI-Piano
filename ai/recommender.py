import sqlite3
import os
from collections import Counter

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_PATH, "database", "piano.db")

def get_recommendations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT notes FROM practice_log")
    rows = cursor.fetchall()
    conn.close()

    all_notes = []
    for row in rows:
        if row[0]:
            all_notes.extend(row[0].split(","))

    if not all_notes:
        return ["C", "D", "E"]

    count = Counter(all_notes)
    weakest = sorted(count, key=count.get)

    return weakest[:3]