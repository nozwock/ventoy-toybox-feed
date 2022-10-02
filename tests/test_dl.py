"""
this is a mess...yaya
i needed logs inside the function so...
"""
import json
import logging
from timeit import default_timer as timer

from rich.logging import RichHandler

from toybox_feed.scrapers.distrowatch import TorrentArchiveScraper
from toybox_feed.utils.dl import USER_AGENT, download_many

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=f"%(message)s",
    datefmt="%H:%M:%S",
    handlers=[RichHandler()],
)


def test_async_download() -> None:
    logger.info("Begin scraping feeds")
    feed = TorrentArchiveScraper().get_feed
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

    # WEIRD...can't use connector obj like this now
    # was able to just a while ago....weird...have to hardcode this in the download fn now
    # now gives error - RuntimeError: Timeout context manager should be used inside a task
    # connector = aiohttp.TCPConnector(force_close=True)
    # can't reuse same tcp connections, distrowatch disconnects otherwise.

    start_time = timer()
    download_many(
        urls,
        "./test_async_download",
        headers={"User-Agent": USER_AGENT, "Connection": "close"},
    )
    logger.info(
        f"[green]{timer() - start_time}s[/green] [yellow]for {len(urls)} urls[/yellow]",
        extra={"markup": True},
    )


if __name__ == "__main__":
    test_async_download()
