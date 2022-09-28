from bs4 import BeautifulSoup
import requests

# from torrentool.api import Torrent

TorrentData = dict[str, str]
# {"name": str, "torrent_url": str, "magnet": str, "date": str}
RawDistroData = tuple[str, tuple]
# (DistroName, RawTorrentData)


class TorrentArchiveScraper:
    """distrowatch.com scraper for its Torrent Archive page"""

    START_URL = "https://www.distrowatch.com/"
    URL = "https://distrowatch.com/dwres.php?resource=bittorrent&sortorder=date"

    def __init__(self) -> None:
        feed: dict[str, list[TorrentData]] = {}
        """
        This is the parsed data.\n
        { 
            "DistroName": [
                {"name": str, "torrent_url": str, "magnet": str, "date": str},
                ...
                ],
            ...
        }
        """

        resp = requests.get(TorrentArchiveScraper.URL)
        soup = BeautifulSoup(resp.text, "lxml")
        resp.close()

        news_feed = soup.find("td", class_="News1").blockquote  # type: ignore
        if news_feed is None:
            raise

        torrent_data = news_feed.find_all("td", class_="torrent")
        release_date = [
            f"{tag.text}".strip()
            for tag in news_feed.find_all("td", class_="torrentdate")
        ]
        raw_feed: zip[RawDistroData] = zip(
            [f"{tag.text}".strip() for tag in torrent_data[::2]],
            [
                (
                    f"{tag.a.text}".strip(),
                    f"{TorrentArchiveScraper.START_URL}{tag.a['href']}".strip(),
                    date,
                )
                for tag, date in zip(torrent_data[1::2], release_date)
            ],
        )

        for distro_data in raw_feed:
            if feed.get(distro_data[0]) is None:
                feed[distro_data[0]] = []
            feed[distro_data[0]].append(
                {
                    "name": distro_data[1][0],
                    "torrent_url": distro_data[1][1],
                    "date": distro_data[1][2],
                }
            )

        # exposing access to the parsed data
        self.get_feed = feed
        """returns parsed data as a dict"""


if __name__ == "__main__":
    from pprint import PrettyPrinter

    # NOTE: pipe the script output with something like `less`
    # since the output is going to be lengthy
    PrettyPrinter().pprint(TorrentArchiveScraper().get_feed)
