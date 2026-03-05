from pathlib import Path

from src.catalog import MovieCatalog


def _dataset_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "movies_small.csv"


def test_load_and_search() -> None:
    catalog = MovieCatalog()
    loaded = catalog.load_csv(_dataset_path())

    assert loaded == 30
    assert catalog.size() == 30

    movie = catalog.search("  the matrix ")
    assert movie is not None
    assert movie.title == "The Matrix"


def test_list_is_alphabetical() -> None:
    catalog = MovieCatalog()
    catalog.load_csv(_dataset_path())

    titles = [movie.title for movie in catalog.list_movies(limit=10)]
    normalized = [title.strip().lower() for title in titles]
    assert normalized == sorted(normalized)


def test_range_and_delete() -> None:
    catalog = MovieCatalog()
    catalog.load_csv(_dataset_path())

    ranged = catalog.range_titles("a", "bzzzz")
    ranged_titles = [movie.title for movie in ranged]
    assert "Avatar" in ranged_titles
    assert "Arrival" in ranged_titles
    assert "Blade Runner 2049" in ranged_titles

    assert catalog.search("Avatar") is not None
    before = catalog.size()
    assert catalog.delete("avatar") is True
    assert catalog.search("Avatar") is None
    assert catalog.size() == before - 1
