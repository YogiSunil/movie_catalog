import argparse
from pathlib import Path

from .catalog import MovieCatalog


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Movie Catalog CLI (AVL-backed)")
    parser.add_argument("--data", default=str(Path("data") / "movies_small.csv"), help="Path to dataset CSV")

    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("title")

    range_parser = subparsers.add_parser("range")
    range_parser.add_argument("low")
    range_parser.add_argument("high")

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--limit", type=int, default=20)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("title")

    subparsers.add_parser("stats")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    catalog = MovieCatalog()
    catalog.load_csv(args.data)

    if args.command == "search":
        movie = catalog.search(args.title)
        print(movie if movie else "Not found")
    elif args.command == "range":
        for movie in catalog.range_titles(args.low, args.high):
            print(movie)
    elif args.command == "list":
        for movie in catalog.list_movies(args.limit):
            print(movie)
    elif args.command == "delete":
        print("Deleted" if catalog.delete(args.title) else "Not found")
    elif args.command == "stats":
        print({"count": catalog.size(), "height": catalog.tree_height()})


if __name__ == "__main__":
    main()
