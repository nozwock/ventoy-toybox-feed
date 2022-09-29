import requests
from pathlib import Path

RESPONSE_OK = 200


def download(url: str, dir: str | Path = "", **kwargs) -> bool:
    """
    True on successful download else False.\n
    **kwargs are passed to requests.get()
    """
    dir = Path(dir) if isinstance(dir, str) else dir
    dir.mkdir(exist_ok=True, parents=True)
    name = url.split("/")[-1]

    response = requests.get(url, **kwargs)
    if response.status_code != RESPONSE_OK:
        return False

    with open(dir.joinpath(name), "wb") as f:
        f.write(response.content)
    return True


if __name__ == "__main__":
    ##############
    # DEBUG TEST #
    ##############
    import logging
    from rich.logging import RichHandler
    from timeit import default_timer as timer

    logging.basicConfig(
        level=logging.INFO,
        format=f"%(message)s",
        datefmt="%H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    log = logging.getLogger(__name__)

    url = (
        "https://www.seoclerk.com/pics/000/923/517/6fe74b36d8230c6581e866362fb435e0.jpg"
    )

    start_time = timer()
    download(url)
    log.info(f"{url}")
    log.info(f"took {timer() - start_time}s")
