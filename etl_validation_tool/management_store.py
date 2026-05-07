from __future__ import annotations

import sqlite3
from dataclasses import asdict
from pathlib import Path

from etl_validation_tool.comparator import ValidationResult


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS test_case (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    external_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    table_pair TEXT NOT NULL,
    query_preview TEXT
);

CREATE TABLE IF NOT EXISTS test_run (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT NOT NULL,
    test_case_id INTEGER NOT NULL,
    source_count INTEGER NOT NULL,
    target_count INTEGER NOT NULL,
    mismatch_count INTEGER NOT NULL,
    pass_status INTEGER NOT NULL,
    generated_sql TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(test_case_id) REFERENCES test_case(id)
);
"""


class TestManagementStore:
    """Simple local test-management persistence similar to lightweight ALM."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(SCHEMA_SQL)

    def register_test_case(self, external_id: str, name: str, table_pair: str, query_preview: str) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO test_case(external_id, name, table_pair, query_preview)
                VALUES (?, ?, ?, ?)
                """,
                (external_id, name, table_pair, query_preview),
            )

    def save_result(self, run_id: str, external_id: str, result: ValidationResult) -> None:
        with self._connect() as conn:
            cur = conn.execute("SELECT id FROM test_case WHERE external_id=?", (external_id,))
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Unknown testcase: {external_id}")
            conn.execute(
                """
                INSERT INTO test_run(run_id, test_case_id, source_count, target_count, mismatch_count, pass_status, generated_sql)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    row[0],
                    result.source_count,
                    result.target_count,
                    result.mismatch_count,
                    int(result.pass_status),
                    result.generated_sql,
                ),
            )

    def latest_results(self) -> list[dict]:
        with self._connect() as conn:
            cur = conn.execute(
                """
                SELECT tc.external_id, tc.name, tr.run_id, tr.source_count, tr.target_count,
                       tr.mismatch_count, tr.pass_status, tr.executed_at
                FROM test_run tr
                JOIN test_case tc ON tc.id = tr.test_case_id
                ORDER BY tr.executed_at DESC
                LIMIT 100
                """
            )
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]
