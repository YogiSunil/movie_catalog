import argparse
from pathlib import Path

from .catalog import MovieCatalog
from .movie import Movie


def _format_movie(movie: Movie) -> str:
    return f"{movie.title} ({movie.year}) | rating={movie.rating} | genres={movie.genres}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Movie Catalog CLI (AVL-backed)")
    parser.add_argument(
        "--data",
        default=str(Path("data") / "movies_small.csv"),
        help="Path to dataset CSV (default: data/movies_small.csv)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Find one movie by exact title")
    search_parser.add_argument("title", help="Movie title to search")

    range_parser = subparsers.add_parser("range", help="List movies in alphabetical title range")
    range_parser.add_argument("low", help="Lower bound title")
    range_parser.add_argument("high", help="Upper bound title")

    list_parser = subparsers.add_parser("list", help="List first N movies alphabetically")
    list_parser.add_argument("n", nargs="?", type=int, default=20, help="Number of items to show (default: 20)")

    delete_parser = subparsers.add_parser("delete", help="Delete one movie by exact title")
    delete_parser.add_argument("title", help="Movie title to delete")

    subparsers.add_parser("stats", help="Show catalog statistics")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    catalog = MovieCatalog()
    loaded = catalog.load_csv(args.data)

    if args.command == "search":
        movie = catalog.search(args.title)
        if movie is None:
            print("Not found")
            return
        print(_format_movie(movie))
    elif args.command == "range":
        movies = catalog.range_titles(args.low, args.high)
        if not movies:
            print("No movies in range")
            return
        for movie in movies:
            print(_format_movie(movie))
    elif args.command == "list":
        movies = catalog.list_movies(args.n)
        if not movies:
            print("Catalog is empty")
            return
        for movie in movies:
            print(_format_movie(movie))
    elif args.command == "delete":
        print("Deleted" if catalog.delete(args.title) else "Not found")
    elif args.command == "stats":
        print(f"Loaded rows: {loaded}")
        print(f"Catalog count: {catalog.size()}")
        print(f"AVL height: {catalog.tree_height()}")


if __name__ == "__main__":
    main()
