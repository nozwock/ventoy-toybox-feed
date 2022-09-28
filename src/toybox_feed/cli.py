import json
from pathlib import Path
from argparse import ArgumentParser
from .scrapers import distrowatch
from timeit import default_timer as timer

DEFAULT_JSON = "feeds.json"


def run() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "-o", "--output", type=str, default=DEFAULT_JSON, metavar="FILE"
    )
    args = parser.parse_args()

    with open(Path(args.output), "w") as f:
        start_time = timer()
        json.dump(distrowatch.TorrentArchiveScraper().get_feed, f)
        print(f"Done! took {timer() - start_time}s")


if __name__ == "__main__":
    run()
