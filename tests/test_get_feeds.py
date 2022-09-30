import json
from pathlib import Path
from pprint import PrettyPrinter

from toybox_feed.helpers import add_magnet_links_to_feeds
from toybox_feed.scrapers.distrowatch import TorrentArchiveScraper


def get_feeds_with_magnets() -> None:
    # with open("./feeds.json", "r") as f:
    #     feed = json.load(f)

    feed = TorrentArchiveScraper().get_feed

    feeds_with_magnets = add_magnet_links_to_feeds(feed)
    with open("feeds_with_magnets.json", "w") as f:
        json.dump(feeds_with_magnets, f)


if __name__ == "__main__":
    get_feeds_with_magnets()
