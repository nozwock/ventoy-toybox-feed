import asyncio
import logging
from pathlib import Path
from typing import Any

import aiofiles
import aiolimiter
import httpx

from toybox_feed.settings import USER_AGENT

logger = logging.getLogger(__name__)

Response = int
Responses = list[int]


def download(
    url: str,
    dir: str | Path = "",
    *,
    headers: dict = None,  # type: ignore
    **kwargs: Any,
) -> Response:
    """
    **kwargs are passed to httpx.get()
    """
    dir = Path(dir) if isinstance(dir, str) else dir
    dir.mkdir(exist_ok=True, parents=True)
    headers = {"User-Agent": USER_AGENT} if headers is None else headers
    filename = url.split("/")[-1]

    response = httpx.get(url, follow_redirects=True, headers=headers, **kwargs)
    if response.status_code != httpx.codes.OK:
        return response.status_code

    with open(dir.joinpath(filename), "wb") as f:
        f.write(response.content)
    return response.status_code


def download_many(
    urls: list[str],
    dir: str | Path = "",
    *,
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
        client: httpx.AsyncClient,
        url: str,
    ) -> None:
        filename = url.split("/")[-1]
        async with semaphore:
            async with limiter:
                logger.info(f"Begin downloading {url}")
                response = await client.get(
                    url,
                    follow_redirects=True,
                )
                responses.append(response.status_code)
                if response.status_code == httpx.codes.OK:
                    async with aiofiles.open(dir.joinpath(filename), "wb") as f:
                        await f.write(response.content)
                        logger.info(
                            f"{response.status_code} Finished downloading {url}"
                        )
                else:
                    logger.error(f"{response.status_code} Failed to download {url}")

    async def main() -> None:
        async with httpx.AsyncClient(headers=headers, **kwargs) as client:
            await asyncio.gather(*[download_task(client, url) for url in urls])

    asyncio.run(main())
    return responses
