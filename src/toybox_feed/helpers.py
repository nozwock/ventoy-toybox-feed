import tempfile
from pathlib import Path

from toybox_feed.scrapers.distrowatch import FeedsItem, TorrentData
from toybox_feed.settings import USER_AGENT
from toybox_feed.utils.dl import download_many
from toybox_feed.utils.torrent import get_magnet_link


def add_magnet_links_to_feeds(
    feeds: dict[str, list[TorrentData]]
) -> dict[str, list[TorrentData]]:

    urls = []
    for torrent_items in feeds.values():
        for item in torrent_items:
            url = item.get(FeedsItem.torrent_url)
            if url is not None:
                urls.append(url)

    map = get_filename_and_feeds_relation(feeds)
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

        for distro_name in map:
            for fname_index_pair in map[distro_name]:
                magnet_link: str | None = get_magnet_link(
                    tmpdir.joinpath(fname_index_pair[0])
                )
                feeds[distro_name][fname_index_pair[1]][FeedsItem.magnet] = magnet_link  # type: ignore

    # OFFLINE DEBUGGING (to not stress the website)
    # tmpdir = Path("./test_async_download")
    # # download_many(urls, tmpdir)

    # for distro_name in map:
    #     for fname_index_pair in map[distro_name]:
    #         # print(fname_index_pair[0])
    #         # print(tmpdir.joinpath(fname_index_pair[0]))
    #         magnet_link: str | None = get_magnet_link(
    #             tmpdir.joinpath(fname_index_pair[0])
    #         )
    #         feeds[distro_name][fname_index_pair[1]]["magnet"] = magnet_link  # type: ignore

    return feeds


FilenameIndexMap = tuple[str, int]
DistroName = str


def get_filename_and_feeds_relation(
    feeds: dict[str, list[TorrentData]]
) -> dict[DistroName, list[FilenameIndexMap]]:
    map: dict[DistroName, list[FilenameIndexMap]] = {}
    for distro_name in feeds:
        if map.get(distro_name) is None:
            map[distro_name] = []
        for i, torrent_item in enumerate(feeds.get(distro_name)):  # type: ignore
            if torrent_item.get(FeedsItem.torrent_url) is None:
                raise ValueError("wth happened?")
            torrent_filename: str = torrent_item.get(FeedsItem.torrent_url).split("/")[-1]  # type: ignore
            map[distro_name].append((torrent_filename, i))
    return map
