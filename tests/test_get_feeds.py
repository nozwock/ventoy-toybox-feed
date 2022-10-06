import json

from toybox_feed.helpers import add_magnet_links_to_feeds, feeds_asdict
from toybox_feed.scrapers.distrowatch import TorrentArchiveScraper


def get_feeds_with_magnets() -> None:
    feeds = TorrentArchiveScraper().feeds

    feeds_with_magnets = add_magnet_links_to_feeds(feeds)
    with open("feeds_with_magnets.json", "w") as f:
        json.dump(feeds_asdict(feeds_with_magnets), f)


if __name__ == "__main__":
    get_feeds_with_magnets()
