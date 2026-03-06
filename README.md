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

## CLI Usage
```bash
python -m src.cli stats
python -m src.cli search "The Matrix"
python -m src.cli range "a" "c"
python -m src.cli list 20
python -m src.cli delete "Avatar"
```

Use a larger dataset:
```bash
python -m src.cli --data data/movies_big.csv stats
```

## Benchmark
```bash
python -m src.benchmark --data data/movies_big.csv --sizes 1000,5000,10000
```

## Step-by-Step Build Plan
See `PROJECT_PLAN.md`.
