"""Central configuration — all values read from environment variables.

Every module imports from here instead of reading os.getenv() directly.
This means there is one place to change a setting and it affects the
entire project. Added to in later stages as new tools are introduced.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = ROOT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ── DuckDB ─────────────────────────────────────────────────────────────────────
DUCKDB_PATH: str = os.getenv("DUCKDB_PATH", str(DATA_DIR / "warehouse.duckdb"))

# ── Ollama — added in Stage 9 ─────────────────────────────────────────────────
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")

# ── Data generation — used from Stage 2 onwards ────────────────────────────────
NUM_EMPLOYEES: int = int(os.getenv("NUM_EMPLOYEES", "5000"))
SEED_YEARS_BACK: int = int(os.getenv("SEED_YEARS_BACK", "3"))
