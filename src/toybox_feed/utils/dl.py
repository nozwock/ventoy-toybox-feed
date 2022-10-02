import asyncio
import logging
from pathlib import Path
from typing import Any

import aiofiles
import aiohttp
import aiolimiter
import requests
from rich.logging import RichHandler

RESPONSE_OK = 200
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64)"

Response = int
Responses = list[int]


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=f"%(message)s",
    datefmt="%H:%M:%S",
    handlers=[RichHandler()],
)


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


def download_many(
    urls: list[str],
    dir: str | Path = "",
    headers: dict = None,  # type: ignore
    rate: float = 1,
    period: float = 0.125,
    sema_value: int = 10,
    **kwargs: Any,
) -> Responses:
    dir = Path(dir) if isinstance(dir, str) else dir
    dir.mkdir(exist_ok=True, parents=True)
    headers = {"User-Agent": USER_AGENT} if headers is None else headers
    semaphore = asyncio.BoundedSemaphore(sema_value)
    limiter = aiolimiter.AsyncLimiter(rate, period)
    responses: Responses = []

    async def download_task(
        session: aiohttp.ClientSession,
        url: str,
    ):
        filename = url.split("/")[-1]
        async with semaphore:
            async with limiter:
                logger.info(f"Begin downloading {url}")
                async with session.get(url) as response:
                    responses.append(response.status)
                    if response.status == RESPONSE_OK:
                        async with aiofiles.open(dir.joinpath(filename), "wb") as f:
                            await f.write(await response.read())
                            logger.info(f"Finished downloading {url}")
                    else:
                        logger.error(f"Failed to download {url}")

    async def main():
        connector = aiohttp.TCPConnector(force_close=True)  # HARDCODED
        # NOTE: find a soln for this later
        async with aiohttp.ClientSession(
            headers=headers, connector=connector, **kwargs
        ) as session:
            await asyncio.gather(*[download_task(session, url) for url in urls])

    asyncio.run(main())
    return responses
