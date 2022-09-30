import requests
from pathlib import Path
from typing import Any

RESPONSE_OK = 200
Response = int


def download(url: str, dir: str | Path = "", **kwargs: Any) -> Response:
    """
    **kwargs are passed to requests.get()
    """
    dir = Path(dir) if isinstance(dir, str) else dir
    dir.mkdir(exist_ok=True, parents=True)
    filename = url.split("/")[-1]

    response = requests.get(url, **kwargs)
    if response.status_code != RESPONSE_OK:
        return response.status_code

    with open(dir.joinpath(filename), "wb") as f:
        f.write(response.content)
    return response.status_code


if __name__ == "__main__":
    ##############
    # DEBUG TEST #
    ##############
    # import json
    import logging
    from rich.logging import RichHandler
    from timeit import default_timer as timer
    from ..scrapers import distrowatch

    logging.basicConfig(
        level=logging.INFO,
        format=f"%(message)s",
        datefmt="%H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    logger = logging.getLogger(__name__)

    # url = (
    #     "https://www.seoclerk.com/pics/000/923/517/6fe74b36d8230c6581e866362fb435e0.jpg"
    # )

    # download(url)
    # with open("feed.json", "r") as f:
    #     feed = json.load(f)
    feed = distrowatch.TorrentArchiveScraper().get_feed

    urls = []
    for v in feed.values():
        urls.append(v[0]["torrent_url"])
    start_time = timer()
    for url in urls:
        download(url, "./torrents-files")
        logger.info(f"{url}")
    logger.info(
        f"[green]{timer() - start_time}s[/green] [yellow]for {len(urls)} urls[/yellow]",
        extra={"markup": True},
    )
