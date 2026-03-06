import csv
from pathlib import Path

src = Path("data/movies_small.csv")
dst = Path("data/movies_big.csv")
target_rows = 10000

with src.open("r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

if not rows:
    raise SystemExit("movies_small.csv is empty")

fieldnames = ["title", "year", "rating", "genres"]
with dst.open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for index in range(target_rows):
        base = rows[index % len(rows)]
        cycle = index // len(rows)
        title = base["title"] if cycle == 0 else f"{base['title']} #{cycle}"
        writer.writerow(
            {
                "title": title,
                "year": base["year"],
                "rating": base["rating"],
                "genres": base["genres"],
            }
        )

print(f"Created {dst} with {target_rows} data rows")
