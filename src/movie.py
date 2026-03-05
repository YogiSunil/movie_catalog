from dataclasses import dataclass


@dataclass(frozen=True)
class Movie:
    title: str
    year: int
    rating: float
    genres: str
