import json
import sqlite3
import math

DB_FILE = "recipes.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cuisine TEXT,
        title TEXT,
        rating REAL,
        prep_time INTEGER,
        cook_time INTEGER,
        total_time INTEGER,
        description TEXT,
        serves TEXT
    )
    """)
    conn.commit()
    conn.close()

def to_number(val):
    """Convert to number or return None if NaN/invalid"""
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return None
        return int(f) if f.is_integer() else f
    except Exception:
        return None

def load_json(path="recipes.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def insert_recipes(data):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    for r in data:
        cur.execute("""
        INSERT INTO recipes (cuisine, title, rating, prep_time, cook_time, total_time, description, serves)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r.get("cuisine"),
            r.get("title"),
            to_number(r.get("rating")),
            to_number(r.get("prep_time")),
            to_number(r.get("cook_time")),
            to_number(r.get("total_time")),
            r.get("description"),
            r.get("serves"),
        ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    data = load_json("recipes.json")
    insert_recipes(data)
    print(f"✅ Loaded {len(data)} recipes into {DB_FILE}")
