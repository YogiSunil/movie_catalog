# PROJECT_PLAN

## Goal
Build a **Movie Catalog Search Engine** using an **AVL TreeMap** in Python.

## Core Data Structure
- `AVLTreeMap` with key = normalized movie title (`strip().lower()`)
- value = `Movie` object
- required operations:
  - `set(key, value)`
  - `get(key)`
  - `delete(key)`
  - `items()` (in-order traversal)
  - `range(low, high)`
  - `__len__()`

## App Layer
- `MovieCatalog` wrapper around AVLTreeMap
- load movies from CSV
- support:
  - exact search by title
  - alphabetical listing
  - title range query
  - delete by title
  - stats (count, height)

## CLI Commands (target)
- `search "The Matrix"`
- `range "A" "C"`
- `list --limit 20`
- `delete "Avatar"`
- `stats`

## Testing Plan
1. Rotation tests:
   - LL, RR, LR, RL cases
2. Invariant tests after random operations:
   - BST ordering
   - balance factor in `{-1, 0, 1}`
   - stored heights are correct
3. Catalog tests:
   - CSV load count
   - exact search
   - range correctness
   - delete correctness

## Benchmark Plan
Compare:
- AVLTreeMap
- naive list
- optional sorted list + `bisect`

Measure for multiple `N`:
- lookup
- insert
- delete
- range

## Delivery Artifacts
1. AVL TreeMap implementation
2. Unit tests + invariant checks
3. Dataset + working CLI app
4. Article + 5-minute presentation material

## Milestones
- Step 1: scaffold repo + project plan + starter dataset
- Step 2: implement AVL insert/get/items/len
- Step 3: add rotations + rebalance tests
- Step 4: implement delete + invariant tests
- Step 5: implement catalog + CLI commands
- Step 6: benchmark + article/presentation assets
