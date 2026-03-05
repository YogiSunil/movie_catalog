from __future__ import annotations

import argparse
import csv
import random
from dataclasses import replace
from pathlib import Path
from time import perf_counter

from .avl_tree_map import AVLTreeMap
from .movie import Movie


def _normalize(title: str) -> str:
    return title.strip().lower()


def _load_movies(path: Path) -> list[Movie]:
    movies: list[Movie] = []
    with open(path, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movies.append(
                Movie(
                    title=row["title"],
                    year=int(row["year"]),
                    rating=float(row["rating"]),
                    genres=row["genres"],
                )
            )
    return movies


def _expand_movies(seed_movies: list[Movie], target_size: int) -> list[Movie]:
    if not seed_movies:
        raise ValueError("Dataset is empty")

    expanded: list[Movie] = []
    index = 0
    while len(expanded) < target_size:
        base = seed_movies[index % len(seed_movies)]
        suffix = index // len(seed_movies)
        if suffix == 0:
            expanded.append(base)
        else:
            expanded.append(replace(base, title=f"{base.title} #{suffix}"))
        index += 1
    return expanded


def _list_set(entries: list[tuple[str, Movie]], key: str, value: Movie) -> None:
    for i, (existing_key, _) in enumerate(entries):
        if existing_key == key:
            entries[i] = (key, value)
            return
    entries.append((key, value))


def _list_get(entries: list[tuple[str, Movie]], key: str) -> Movie | None:
    for existing_key, movie in entries:
        if existing_key == key:
            return movie
    return None


def _list_delete(entries: list[tuple[str, Movie]], key: str) -> bool:
    for i, (existing_key, _) in enumerate(entries):
        if existing_key == key:
            entries.pop(i)
            return True
    return False


def _list_range(entries: list[tuple[str, Movie]], low: str, high: str) -> list[tuple[str, Movie]]:
    filtered = [(k, v) for k, v in entries if low <= k <= high]
    return sorted(filtered, key=lambda item: item[0])


def _time_call(action: callable) -> float:
    start = perf_counter()
    action()
    return (perf_counter() - start) * 1000.0


def _benchmark_avl(
    base_movies: list[Movie],
    lookup_ops: int,
    insert_ops: int,
    delete_ops: int,
    range_ops: int,
    rng: random.Random,
) -> dict[str, float]:
    tree: AVLTreeMap[str, Movie] = AVLTreeMap()

    build_ms = _time_call(lambda: [tree.set(_normalize(movie.title), movie) for movie in base_movies])
    keys = [_normalize(movie.title) for movie in base_movies]

    lookup_keys = [rng.choice(keys) for _ in range(lookup_ops)]
    lookup_ms = _time_call(lambda: [tree.get(key) for key in lookup_keys])

    insert_movies = [
        Movie(title=f"Inserted AVL {i:05d}", year=2026, rating=7.0, genres="Benchmark") for i in range(insert_ops)
    ]
    insert_ms = _time_call(lambda: [tree.set(_normalize(movie.title), movie) for movie in insert_movies])

    delete_candidates = keys[:]
    rng.shuffle(delete_candidates)
    delete_keys = delete_candidates[:delete_ops]
    delete_ms = _time_call(lambda: [tree.delete(key) for key in delete_keys])

    remaining_keys = sorted([k for k, _ in tree.items()])
    if not remaining_keys:
        range_ms = 0.0
    else:
        range_bounds: list[tuple[str, str]] = []
        for _ in range(range_ops):
            i = rng.randrange(len(remaining_keys))
            j = rng.randrange(len(remaining_keys))
            low = remaining_keys[min(i, j)]
            high = remaining_keys[max(i, j)]
            range_bounds.append((low, high))
        range_ms = _time_call(lambda: [list(tree.range(low, high)) for low, high in range_bounds])

    return {
        "build": build_ms,
        "lookup": lookup_ms,
        "insert": insert_ms,
        "delete": delete_ms,
        "range": range_ms,
    }


def _benchmark_list(
    base_movies: list[Movie],
    lookup_ops: int,
    insert_ops: int,
    delete_ops: int,
    range_ops: int,
    rng: random.Random,
) -> dict[str, float]:
    entries: list[tuple[str, Movie]] = []

    def build() -> None:
        for movie in base_movies:
            _list_set(entries, _normalize(movie.title), movie)

    build_ms = _time_call(build)
    keys = [_normalize(movie.title) for movie in base_movies]

    lookup_keys = [rng.choice(keys) for _ in range(lookup_ops)]
    lookup_ms = _time_call(lambda: [_list_get(entries, key) for key in lookup_keys])

    insert_movies = [
        Movie(title=f"Inserted List {i:05d}", year=2026, rating=7.0, genres="Benchmark") for i in range(insert_ops)
    ]

    def insert_action() -> None:
        for movie in insert_movies:
            _list_set(entries, _normalize(movie.title), movie)

    insert_ms = _time_call(insert_action)

    delete_candidates = keys[:]
    rng.shuffle(delete_candidates)
    delete_keys = delete_candidates[:delete_ops]
    delete_ms = _time_call(lambda: [_list_delete(entries, key) for key in delete_keys])

    remaining_keys = sorted([key for key, _ in entries])
    if not remaining_keys:
        range_ms = 0.0
    else:
        range_bounds: list[tuple[str, str]] = []
        for _ in range(range_ops):
            i = rng.randrange(len(remaining_keys))
            j = rng.randrange(len(remaining_keys))
            low = remaining_keys[min(i, j)]
            high = remaining_keys[max(i, j)]
            range_bounds.append((low, high))
        range_ms = _time_call(lambda: [_list_range(entries, low, high) for low, high in range_bounds])

    return {
        "build": build_ms,
        "lookup": lookup_ms,
        "insert": insert_ms,
        "delete": delete_ms,
        "range": range_ms,
    }


def _print_table(size: int, avl_metrics: dict[str, float], list_metrics: dict[str, float]) -> None:
    print(f"\nN = {size}")
    print("Structure | Build(ms) | Lookup(ms) | Insert(ms) | Delete(ms) | Range(ms)")
    print("-" * 72)
    print(
        f"AVL      | {avl_metrics['build']:9.2f} | {avl_metrics['lookup']:10.2f} | "
        f"{avl_metrics['insert']:10.2f} | {avl_metrics['delete']:10.2f} | {avl_metrics['range']:9.2f}"
    )
    print(
        f"List     | {list_metrics['build']:9.2f} | {list_metrics['lookup']:10.2f} | "
        f"{list_metrics['insert']:10.2f} | {list_metrics['delete']:10.2f} | {list_metrics['range']:9.2f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark AVL tree map against a naive list baseline")
    parser.add_argument(
        "--data",
        default=str(Path("data") / "movies_small.csv"),
        help="CSV dataset path (title,year,rating,genres)",
    )
    parser.add_argument(
        "--sizes",
        default="1000,5000,10000",
        help="Comma-separated dataset sizes to benchmark",
    )
    parser.add_argument("--lookups", type=int, default=10000)
    parser.add_argument("--inserts", type=int, default=2000)
    parser.add_argument("--deletes", type=int, default=2000)
    parser.add_argument("--ranges", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    sizes = [int(part.strip()) for part in args.sizes.split(",") if part.strip()]
    source_movies = _load_movies(Path(args.data))
    rng = random.Random(args.seed)

    print("Benchmark: AVLTreeMap vs Naive List")
    print(
        f"Operations per run: lookups={args.lookups}, inserts={args.inserts}, "
        f"deletes={args.deletes}, ranges={args.ranges}"
    )

    for size in sizes:
        movies = _expand_movies(source_movies, size)
        avl_metrics = _benchmark_avl(movies, args.lookups, args.inserts, args.deletes, args.ranges, rng)
        list_metrics = _benchmark_list(movies, args.lookups, args.inserts, args.deletes, args.ranges, rng)
        _print_table(size, avl_metrics, list_metrics)


if __name__ == "__main__":
    main()
