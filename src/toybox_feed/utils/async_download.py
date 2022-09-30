import asyncio
import aiohttp
import aiofiles
import aiolimiter
from pathlib import Path
from typing import Any


USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64)"
Responses = list[int]


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
                if response.status == 200:
                    f = await aiofiles.open(dir.joinpath(filename), "wb")
                    await f.write(await response.read())
                    logger.info(f"Finished downloading {url}")
                    await f.close()
                else:
                    logger.error(f"Failed to download {url}")
                semaphore.release()

    async def main() -> None:
        """async file download function."""
        async with aiohttp.ClientSession(headers=headers, **kwargs) as session:
            await asyncio.gather(*[fetch_file(session, url) for url in urls])

    asyncio.run(main())
    return responses


if __name__ == "__main__":
    ###############
    # DEBUG TESTS #
    ###############
    import json
    import logging
    from rich.logging import RichHandler
    from timeit import default_timer as timer
    from ..scrapers import distrowatch

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format=f"%(message)s",
        datefmt="%H:%M:%S",
        handlers=[RichHandler()],
    )

    feed = distrowatch.TorrentArchiveScraper().get_feed
    # with open("feed.json", "r") as f:
    #     feed = json.load(f)

    urls = []
    for v in feed.values():
        urls.append(v[0].get("torrent_url"))

    start_time = timer()
    download_many(urls, "./torrent-files-async2")
    logger.info(
        f"[green]{timer() - start_time}s[/green] [yellow]for {len(urls)} urls[/yellow]",
        extra={"markup": True},
    )
