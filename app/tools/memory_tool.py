import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path("app/memory/memory.db")


def init_memory_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trace_id TEXT NOT NULL,
            user_idea TEXT NOT NULL,
            plan TEXT,
            market_analysis TEXT,
            product_analysis TEXT,
            critic_review TEXT,
            final_report TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_run_to_memory(
    trace_id: str,
    user_idea: str,
    plan: str,
    market_analysis: str,
    product_analysis: str,
    critic_review: str,
    final_report: str,
) -> None:
    init_memory_db()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO runs (
            trace_id,
            user_idea,
            plan,
            market_analysis,
            product_analysis,
            critic_review,
            final_report,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            trace_id,
            user_idea,
            plan,
            market_analysis,
            product_analysis,
            critic_review,
            final_report,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )

    connection.commit()
    connection.close()


def get_last_runs(limit: int = 5) -> list[dict]:
    init_memory_db()

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, trace_id, user_idea, created_at
        FROM runs
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    connection.close()

    return [dict(row) for row in rows]