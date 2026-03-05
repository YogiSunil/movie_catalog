from __future__ import annotations

import csv
from pathlib import Path
from typing import List, Optional

from .avl_tree_map import AVLTreeMap
from .movie import Movie


class MovieCatalog:
    def __init__(self) -> None:
        self._tree: AVLTreeMap[str, Movie] = AVLTreeMap()

    @staticmethod
    def _normalize(title: str) -> str:
        return title.strip().lower()

    def add_movie(self, movie: Movie) -> None:
        self._tree.set(self._normalize(movie.title), movie)

    def search(self, title: str) -> Optional[Movie]:
        return self._tree.get(self._normalize(title))

    def delete(self, title: str) -> bool:
        return self._tree.delete(self._normalize(title))

    def list_movies(self, limit: Optional[int] = None) -> List[Movie]:
        movies = [movie for _, movie in self._tree.items()]
        return movies if limit is None else movies[:limit]

    def range_titles(self, low: str, high: str) -> List[Movie]:
        return [movie for _, movie in self._tree.range(self._normalize(low), self._normalize(high))]

    def load_csv(self, path: str | Path) -> int:
        count = 0
        with open(path, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                movie = Movie(
                    title=row["title"],
                    year=int(row["year"]),
                    rating=float(row["rating"]),
                    genres=row["genres"],
                )
                self.add_movie(movie)
                count += 1
        return count

    def size(self) -> int:
        return len(self._tree)

    def tree_height(self) -> int:
        return self._tree.height()
