import json
from pathlib import Path
from argparse import ArgumentParser
from scrapers import distrowatch
import timeit

DEFAULT_JSON = "feed.json"

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-o", "--output", type=str, default=DEFAULT_JSON, metavar="FILE"
    )
    args = parser.parse_args()

    with open(Path(args.output), "w") as f:
        start_time = timeit.default_timer()
        json.dump(distrowatch.TorrentArchiveScraper().feed, f)
        print(f"Done! took {timeit.default_timer() - start_time}s")
