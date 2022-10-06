import dataclasses
import tempfile
from pathlib import Path

from toybox_feed.scrapers.distrowatch import FeedsItem
from toybox_feed.settings import USER_AGENT
from toybox_feed.utils.dl import download_many
from toybox_feed.utils.torrent import get_magnet_link


def feeds_asdict(feeds: list[FeedsItem]) -> list[dict[str, str]]:
    return [dataclasses.asdict(feeds_item) for feeds_item in feeds]


def add_magnet_links_to_feeds(feeds: list[FeedsItem]) -> list[FeedsItem]:

    urls = []
    for item in feeds:
        url = item.torrent_url
        if url is not None:
            urls.append(url)

    maps = get_filename_and_feeds_relation(feeds)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        download_many(
            urls,
            tmpdir,
            headers={"User-Agent": USER_AGENT, "Connection": "close"},
            rate=1,
            period=0.4,  # this rps works fine on ghub actions (distrowatch doesn't get angry T~T)
        )
        # turning off HTTP keep-alive...tho didn't I already did that with TCPConnector?
        # hopefully this fixes Connection reset errors

        for name_index_map in maps:
            magnet_link: str | None = get_magnet_link(
                tmpdir.joinpath(name_index_map[0])
            )
            feeds[name_index_map[1]].magnet = magnet_link

    ###############################################
    # for OFFLINE DEBUGGING (to not stress the website)
    # tmpdir = Path("./test_async_download")

    # for name_index_map in maps:
    #     magnet_link: str | None = get_magnet_link(tmpdir.joinpath(name_index_map[0]))
    #     feeds[name_index_map[1]].magnet = magnet_link
    ###############################################

    return feeds


NameIndexMap = tuple[str, int]


def get_filename_and_feeds_relation(feeds: list[FeedsItem]) -> list[NameIndexMap]:
    map: list[NameIndexMap] = []
    for i, item in enumerate(feeds):
        name = item.name
        if name is None:
            raise ValueError("name doesn't exists?")
        map.append((name, i))
    return map
