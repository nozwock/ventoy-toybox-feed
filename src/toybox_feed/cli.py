import json
import logging
from argparse import ArgumentParser
from pathlib import Path
from timeit import default_timer as timer

from toybox_feed.helpers import add_magnet_links_to_feeds, feeds_asdict
from toybox_feed.scrapers.distrowatch import TorrentArchiveScraper
from toybox_feed.settings import DEFAULT_JSON

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "-o", "--output", type=str, default=DEFAULT_JSON, metavar="FILE"
    )
    args = parser.parse_args()

    with open(Path(args.output), "w") as f:
        start_time = timer()
        logger.info("Begin scraping feeds")
        feeds = TorrentArchiveScraper().feeds
        logger.info("Finished scraping feeds")
        feeds = add_magnet_links_to_feeds(feeds)
        json.dump(feeds_asdict(feeds), f)
        print(f"Done! took {timer() - start_time}s")


if __name__ == "__main__":
    run()
