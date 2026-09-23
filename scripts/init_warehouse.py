#!/usr/bin/env python3
"""Stage 1 — DuckDB warehouse schema initialisation.

Creates the four raw ingestion tables. Run this once before any other step.
Safe to re-run — all statements use IF NOT EXISTS.

Note: AI output tables (ai_attrition_alerts, ai_dept_reports) are NOT here.
They will be added in Stage 9 when the AI layer is built. Keeping schema
changes tied to the feature that needs them makes the git history readable.

Usage:
    python scripts/init_warehouse.py
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ingestion.config import DUCKDB_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("init_warehouse")

# ── DDL — raw ingestion tables only ────────────────────────────────────────────
DDL = """
CREATE TABLE IF NOT EXISTS raw_departments (
    dept_id           VARCHAR PRIMARY KEY,
    department        VARCHAR NOT NULL,
    division          VARCHAR,
    head_count_target INTEGER,
    cost_center       VARCHAR,
    location          VARCHAR,
    loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_employees (
    emp_id       VARCHAR PRIMARY KEY,
    name         VARCHAR NOT NULL,
    gender       VARCHAR,
    department   VARCHAR,
    designation  VARCHAR,
    band         VARCHAR,
    salary       DOUBLE,
    location     VARCHAR,
    joining_date DATE,
    status       VARCHAR DEFAULT 'active',
    exit_date    DATE,
    loaded_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_performance_reviews (
    review_id      VARCHAR PRIMARY KEY,
    emp_id         VARCHAR NOT NULL,
    review_quarter VARCHAR,
    review_date    DATE,
    rating         DOUBLE,
    kpi_score      DOUBLE,
    training_hours INTEGER,
    promotion_flag BOOLEAN,
    manager_id     VARCHAR,
    dept_id        VARCHAR,
    loaded_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_attendance (
    att_id        VARCHAR PRIMARY KEY,
    emp_id        VARCHAR NOT NULL,
    att_date      DATE    NOT NULL,
    status        VARCHAR,
    hours_worked  DOUBLE,
    overtime_flag BOOLEAN,
    late_arrival  BOOLEAN,
    loaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def main() -> None:
    logger.info("Connecting to DuckDB at: %s", DUCKDB_PATH)
    conn = duckdb.connect(DUCKDB_PATH)

    try:
        conn.execute(DDL)
        conn.commit()

        tables = conn.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'main' ORDER BY table_name"
        ).fetchall()

        logger.info("Tables in warehouse:")
        for (name,) in tables:
            logger.info("  ✓ %s", name)

    finally:
        conn.close()

    logger.info("Done. Next step: Stage 2 — add Pydantic models and data generator.")


if __name__ == "__main__":
    main()
