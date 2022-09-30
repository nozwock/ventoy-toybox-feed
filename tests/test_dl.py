"""
this is a mess...yaya
i needed logs inside the function so...
"""
# from toybox_feed.utils.dl import download_many
import asyncio
import logging
from pathlib import Path
from timeit import default_timer as timer
from typing import Any

import aiofiles
import aiohttp
import aiolimiter
from rich.logging import RichHandler

from toybox_feed.scrapers.distrowatch import TorrentArchiveScraper
from toybox_feed.utils.dl import RESPONSE_OK, USER_AGENT, Responses

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=f"%(message)s",
    datefmt="%H:%M:%S",
    handlers=[RichHandler()],
)


def download_many(
    urls: list[str],
    dir: str | Path = "",
    headers: dict = None,  # type: ignore
    semaphore: asyncio.Semaphore = None,  # type: ignore
    limiter: aiolimiter.AsyncLimiter = None,  # type: ignore
    **kwargs: Any,
) -> Responses:
    dir = Path(dir) if isinstance(dir, str) else dir
    dir.mkdir(exist_ok=True, parents=True)
    headers = {"User-Agent": USER_AGENT} if headers is None else headers
    semaphore = asyncio.Semaphore(5) if semaphore is None else semaphore
    limiter = aiolimiter.AsyncLimiter(1, 0.125) if limiter is None else limiter
    responses: Responses = []

    async def fetch_file(
        session: aiohttp.ClientSession,
        url: str,
    ) -> None:
        filename = url.split("/")[-1]
        await semaphore.acquire()
        async with limiter:
            logger.info(f"Begin downloading {url}")
            async with session.get(url) as response:
                logger.info(f"Received response {response.status}")
                responses.append(response.status)
                if response.status == RESPONSE_OK:
                    f = await aiofiles.open(dir.joinpath(filename), "wb")
                    await f.write(await response.read())
                    logger.info(f"Finished downloading {url}")
                    await f.close()
                else:
                    logger.error(f"Failed to download {url}")
                semaphore.release()

    async def main() -> None:
        async with aiohttp.ClientSession(headers=headers, **kwargs) as session:
            await asyncio.gather(*[fetch_file(session, url) for url in urls])

    asyncio.run(main())
    return responses


def test_async_download() -> None:
    feed = TorrentArchiveScraper().get_feed
    urls = []
    for v in feed.values():
        url = v[0].get("torrent_url")
        if url is not None:
            urls.append(url)

    start_time = timer()
    download_many(urls, "./test_async_download")
    logger.info(
        f"[green]{timer() - start_time}s[/green] [yellow]for {len(urls)} urls[/yellow]",
        extra={"markup": True},
    )


if __name__ == "__main__":
    test_async_download()
