import sqlite3
from typing import Optional
from fastapi import FastAPI, Query

app = FastAPI(title="Recipe API (SQLite)", version="1.0")

DB_FILE = "recipes.db"

def get_conn():
    return sqlite3.connect(DB_FILE)

@app.get("/api/recipes")
def get_recipes(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=50)):
    """Get paginated recipes sorted by rating"""
    conn = get_conn()
    cur = conn.cursor()
    total = cur.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
    offset = (page - 1) * limit
    cur.execute("""
        SELECT id, title, cuisine, rating, total_time, serves
        FROM recipes
        ORDER BY rating DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))
    rows = cur.fetchall()
    conn.close()
    data = [
        {"id": r[0], "title": r[1], "cuisine": r[2], "rating": r[3],
         "total_time": r[4], "serves": r[5]} for r in rows
    ]
    return {"page": page, "limit": limit, "total": total, "data": data}

@app.get("/api/recipes/search")
def search_recipes(
    title: Optional[str] = None,
    cuisine: Optional[str] = None,
    rating: Optional[float] = None,
    total_time: Optional[int] = None,
):
    """Search recipes by filters"""
    conn = get_conn()
    cur = conn.cursor()
    query = "SELECT id, title, cuisine, rating, total_time, serves FROM recipes WHERE 1=1"
    params = []
    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")
    if cuisine:
        query += " AND cuisine = ?"
        params.append(cuisine)
    if rating is not None:
        query += " AND rating >= ?"
        params.append(rating)
    if total_time is not None:
        query += " AND total_time <= ?"
        params.append(total_time)
    query += " ORDER BY rating DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    data = [
        {"id": r[0], "title": r[1], "cuisine": r[2], "rating": r[3],
         "total_time": r[4], "serves": r[5]} for r in rows
    ]
    return {"data": data}
