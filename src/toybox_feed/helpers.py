import tempfile
from pathlib import Path

from toybox_feed.scrapers.distrowatch import FeedsConf, FeedsItem
from toybox_feed.settings import USER_AGENT
from toybox_feed.utils.dl import download_many
from toybox_feed.utils.torrent import get_magnet_link


def add_magnet_links_to_feeds(feeds: list[FeedsItem]) -> list[FeedsItem]:

    urls = []
    for torrent_item in feeds:
        url = torrent_item.get(FeedsConf.torrent_url)
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
            feeds[name_index_map[1]][FeedsConf.magnet] = magnet_link  # type: ignore

    ###############################################
    # for OFFLINE DEBUGGING (to not stress the website)
    # tmpdir = Path("./test_async_download")

    # for name_index_map in maps:
    #     magnet_link: str | None = get_magnet_link(tmpdir.joinpath(name_index_map[0]))
    #     feeds[name_index_map[1]][FeedsItem.magnet] = magnet_link  # type: ignore
    ###############################################

    return feeds


NameIndexMap = tuple[str, int]


def get_filename_and_feeds_relation(feeds: list[FeedsItem]) -> list[NameIndexMap]:
    map: list[NameIndexMap] = []
    for i, item in enumerate(feeds):
        name: str | None = item.get(FeedsConf.name)
        if name is None:
            raise ValueError("name doesn't exists?")
        map.append((name, i))
    return map
