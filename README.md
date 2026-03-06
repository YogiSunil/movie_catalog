# Movie AVL Catalog

Movie AVL Catalog is a Movie Search Engine that uses an AVL TreeMap (self-balancing binary search tree) to store and retrieve movies by title.

## What This Project Does
- Stores movies keyed by normalized title (case-insensitive)
- Supports exact search, delete, alphabetical listing, and title range queries
- Demonstrates AVL tree scalability against a naive list baseline with benchmarks

## Tech Used
- Python
- pytest (unit testing)

## Data Used
- data/movies_small.csv: small dataset for correctness and CLI demos
- data/movies_big.csv: larger generated dataset for scalability benchmarks

CSV schema:
- title, year, rating, genres

## Implemented Features

### AVL TreeMap
- set(key, value)
- get(key)
- delete(key)
- items() in sorted key order
- range(low, high)
- __len__()

### Movie Catalog CLI
- search "The Matrix"
- range "a" "c"
- list 20
- delete "Avatar"
- stats

### Test Coverage
- Rotation tests: LL, RR, LR, RL
- AVL invariant tests after random inserts/deletes
- Catalog tests for load/search/range/delete

### Benchmark
- Compares AVLTreeMap vs naive list on:
	- build/load
	- lookup
	- insert
	- delete
	- range queries

## Project Structure
- src/: AVL tree, domain model, catalog wrapper, CLI, benchmark, dataset generator
- tests/: rotation, invariant, and catalog tests
- data/: movie datasets
- article/: article draft and diagrams folder

## Setup

From project root:

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## How To Run

Run tests:

```bash
python -m pytest -q
```

Run CLI commands:

```bash
python -m src.cli stats
python -m src.cli search "The Matrix"
python -m src.cli range "a" "c"
python -m src.cli list 20
python -m src.cli delete "Avatar"
```

Run CLI with larger dataset:

```bash
python -m src.cli --data data/movies_big.csv stats
```

Generate/re-generate large dataset:

```bash
python src/generate_big_dataset.py
```

Run benchmark:

```bash
python -m src.benchmark --data data/movies_big.csv --sizes 1000,5000,10000
```

## Why AVL Here
- Naive list lookup is O(n)
- AVL lookup/insert/delete are O(log n)
- AVL naturally supports ordered traversal and efficient range queries
