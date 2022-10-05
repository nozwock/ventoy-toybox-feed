from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from toybox_feed.settings import USER_AGENT

FeedsItem = dict[str, str]
# {"group": str, "name": str, "torrent_url": str, "magnet": str, "date": str}
RawFeedsItem = tuple[str, tuple]
# (group, (name, torrent_url, date))


@dataclass(frozen=True)
class FeedsConf:
    group = "group"
    name = "name"
    torrent_url = "torrent_url"
    magnet = "magnet"
    date = "date"


class TorrentArchiveScraper:
    """distrowatch.com scraper for its Torrent Archive page"""

    START_URL = "https://www.distrowatch.com/"
    URL = "https://distrowatch.com/dwres.php?resource=bittorrent&sortorder=date"

    def __init__(self) -> None:
        self.__feeds: list[FeedsItem] = []
        """
        This is the structure of parsed data.\n
        [ 
            {
                "group": str,
                "name": str,
                "torrent_url": str,
                "date": str
                "magnet": str,
            },
            ...
        ]
        """

        resp = requests.get(
            TorrentArchiveScraper.URL,
            headers={"User-Agent": USER_AGENT},
            timeout=5,
        )
        soup = BeautifulSoup(resp.text, "lxml")
        resp.close()

        td_blockquote = soup.find("td", class_="News1").blockquote  # type: ignore
        if td_blockquote is None:
            raise

        torrent_data = td_blockquote.find_all("td", class_="torrent")
        release_dates = [
            f"{tag.text}".strip()
            for tag in td_blockquote.find_all("td", class_="torrentdate")
        ]
        raw_feeds: zip[RawFeedsItem] = zip(
            [f"{tag.text}".strip() for tag in torrent_data[::2]],  # distro/group name
            [
                (
                    f"{tag.a.text}".strip(),  # filename or name
                    f"{TorrentArchiveScraper.START_URL}{tag.a['href']}".strip(),  # torrent url
                    date,  # release date
                )
                for tag, date in zip(torrent_data[1::2], release_dates)
            ],
        )

        for feeds_item in raw_feeds:
            self.__feeds.append(
                {
                    FeedsConf.group: feeds_item[0],
                    FeedsConf.name: feeds_item[1][0],
                    FeedsConf.torrent_url: feeds_item[1][1],
                    FeedsConf.date: feeds_item[1][2],
                }
            )

    @property
    def feeds(self) -> list[FeedsItem]:
        return self.__feeds


if __name__ == "__main__":
    from pprint import PrettyPrinter

    # NOTE: pipe the script output with something like `less`
    # since the output is going to be lengthy
    PrettyPrinter().pprint(TorrentArchiveScraper().feeds)
