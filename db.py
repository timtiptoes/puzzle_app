import sqlite3
from datetime import datetime

DB_PATH = "puzzles.db"

_CREATE = """
CREATE TABLE IF NOT EXISTS puzzle_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  TEXT    NOT NULL,
    clue        TEXT    NOT NULL,
    puzzle_type TEXT    NOT NULL
)
"""


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(_CREATE)


def log_puzzle(clue, puzzle_type):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO puzzle_log (created_at, clue, puzzle_type) VALUES (?, ?, ?)",
            (datetime.now().isoformat(timespec="seconds"), clue, puzzle_type),
        )


def get_log(page=1, per_page=25):
    offset = (page - 1) * per_page
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        total = conn.execute("SELECT COUNT(*) FROM puzzle_log").fetchone()[0]
        rows = conn.execute(
            "SELECT id, created_at, clue, puzzle_type FROM puzzle_log"
            " ORDER BY id DESC LIMIT ? OFFSET ?",
            (per_page, offset),
        ).fetchall()
    return rows, total
