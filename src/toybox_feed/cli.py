import json
from argparse import ArgumentParser
from pathlib import Path
from timeit import default_timer as timer

from toybox_feed.helpers import add_magnet_links_to_feeds
from toybox_feed.scrapers import distrowatch

DEFAULT_JSON = "feeds.json"


def run() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "-o", "--output", type=str, default=DEFAULT_JSON, metavar="FILE"
    )
    args = parser.parse_args()

    with open(Path(args.output), "w") as f:
        start_time = timer()
        feeds = add_magnet_links_to_feeds(distrowatch.TorrentArchiveScraper().feeds)
        json.dump(feeds, f)
        print(f"Done! took {timer() - start_time}s")


if __name__ == "__main__":
    run()
