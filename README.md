# HRFlow — Workforce Analytics Data Warehouse

A data engineering project built with **Apache Airflow**, **dbt Core**,
**DuckDB** (Snowflake-equivalent, free and local), **Python**, and **Ollama** (local LLM).

> **Stage 1 of 10** — Project scaffold and warehouse schema initialised.
> Subsequent stages add the ingestion pipeline, dbt models, Airflow DAGs, and AI layer.

---

## Planned tech stack

| Layer | Tool | Stage |
|---|---|---|
| Warehouse | DuckDB (Snowflake-equivalent, free local) | ← this stage |
| Ingestion | Python + Faker + Pydantic | 2–3 |
| Transformation | dbt Core + dbt-duckdb adapter | 4–7 |
| Orchestration | Apache Airflow | 8 |
| AI | Ollama (local LLM) | 9 |
| Containers | Docker Compose | 8 |
| CI/CD | GitHub Actions | 10 |

---

## Prerequisites

| Tool | Version | Check |
|---|---|---|
| Python | 3.11+ | `python --version` |
| pip | latest | `pip --version` |
| Git | any | `git --version` |
| Docker Desktop | latest | needed from Stage 8 |
| Ollama | latest | needed from Stage 9 |

---

## Virtual environment

Create a venv:
```bash
python -m venv .venv
```

Activate it:
```bash
# Windows PowerShell
.venv\Scripts\activate (or) \.venv\Scripts\Activate.ps1 (or) .\.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

Deactivate it:
```bash
deactivate
```

---

## Setup (Stage 1)

```bash
pip install -r requirements.txt  # 1. install dependencies
cp .env.example .env             # 2. copy env file (Windows)
python scripts/init_warehouse.py # 3. create warehouse tables
```

Verify the warehouse was created:

```powershell
@'
import duckdb
conn = duckdb.connect("data/warehouse.duckdb")
tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
print([t[0] for t in tables])
'@ | python -
```

## Expected: ['raw_attendance', 'raw_departments', 'raw_employees', 'raw_performance_reviews']

---

## Project structure

```
HRFlow/
├── ingestion/               # Python ingestion pipeline — Stages 2–3
│   ├── __init__.py
│   └── config.py            # central config (paths, env vars)
├── ai/                      # LLM integration — Stage 9
│   └── __init__.py
├── dags/                    # Airflow DAGs — Stage 8
├── dbt/                     # dbt project — Stages 4–7
│   ├── dbt_project.yml
│   └── profiles.yml
├── scripts/
│   └── init_warehouse.py    # one-time: creates DuckDB raw tables
├── data/                    # DuckDB warehouse file (git-ignored)
├── tests/                   # pytest suite — Stage 10
├── requirements.txt
├── .env.example
└── Makefile
```
