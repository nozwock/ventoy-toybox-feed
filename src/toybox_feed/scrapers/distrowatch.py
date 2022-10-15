from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from toybox_feed.settings import USER_AGENT


@dataclass(kw_only=True)
class FeedsItem:
    group: str | None = None
    name: str | None = None
    torrent_url: str | None = None
    magnet: str | None = None
    date: str | None = None


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
                "magnet": str,
                "date": str
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
        date_fields = [
            f"{tag.text}".strip()
            for tag in td_blockquote.find_all("td", class_="torrentdate")
        ]

        group_fields = map(lambda t: f"{t.text}".strip(), torrent_data[::2])
        name_fields, torrent_url_fields = (
            map(lambda t: f"{t.a.text}".strip(), torrent_data[1::2]),
            map(
                lambda t: f"{TorrentArchiveScraper.START_URL}{t.a['href']}".strip(),
                torrent_data[1::2],
            ),
        )

        for group, name, torrent_url, date in zip(
            group_fields, name_fields, torrent_url_fields, date_fields
        ):
            self.__feeds.append(
                FeedsItem(group=group, name=name, torrent_url=torrent_url, date=date)
            )

    @property
    def feeds(self) -> list[FeedsItem]:
        return self.__feeds


if __name__ == "__main__":
    from pprint import PrettyPrinter

    from toybox_feed import helpers

    # NOTE: pipe the script output with something like `less`
    # since the output is going to be lengthy
    PrettyPrinter().pprint(helpers.feeds_asdict(TorrentArchiveScraper().feeds))
