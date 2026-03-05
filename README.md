# Movie AVL Catalog

Movie Catalog Search Engine powered by an AVL TreeMap.

## Tech
- Python 3.11+
- `pytest` for tests

## Project Structure
- `src/` AVL tree, catalog domain, CLI, benchmark
- `tests/` rotation, invariant, and catalog tests
- `data/` small and later large movie datasets
- `article/` write-up and presentation assets

## Quick Start
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

## Step-by-Step Build Plan
See `PROJECT_PLAN.md`.
