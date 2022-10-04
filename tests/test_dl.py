import json
import logging
from timeit import default_timer as timer

from rich.logging import RichHandler

from toybox_feed.scrapers.distrowatch import TorrentArchiveScraper
from toybox_feed.settings import USER_AGENT
from toybox_feed.utils.dl import download_many

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=f"%(message)s",
    datefmt="%H:%M:%S",
    handlers=[RichHandler()],
)


def test_async_download() -> None:
    logger.info("Begin scraping feeds")
    feed = TorrentArchiveScraper().feeds
    logger.info(
        "[bold green]Finished scraping feeds[/bold green]", extra={"markup": True}
    )

    with open("base_feeds.json", "w") as f:
        json.dump(feed, f)

    urls = []
    for torrent_items in feed.values():
        for item in torrent_items:
            url = item.get("torrent_url")
            if url is not None:
                urls.append(url)

    start_time = timer()
    download_many(
        urls,
        "./test_async_download",
        headers={"User-Agent": USER_AGENT, "Connection": "close"},
        period=0.4,
    )
    logger.info(
        f"[green]{timer() - start_time}s[/green] [yellow]for {len(urls)} urls[/yellow]",
        extra={"markup": True},
    )


if __name__ == "__main__":
    test_async_download()
