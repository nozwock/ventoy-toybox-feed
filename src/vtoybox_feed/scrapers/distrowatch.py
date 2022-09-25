from bs4 import BeautifulSoup
import requests

# from torrentool.api import Torrent
# from enum import Enum

TorrentData = dict[str, str]
# {"name": str, "torrent_url": str, "magnet": str, "date": str}
RawDistroData = tuple[str, tuple]
# (DistroName, RawTorrentData)


class TorrentArchiveScraper:
    """distrowatch.com scraper for its Torrent Archive page"""

    START_URL = "https://www.distrowatch.com/"
    URL = "https://distrowatch.com/dwres.php?resource=bittorrent&sortorder=date"

    def __init__(self) -> None:
        self.feed: dict[str, list[TorrentData]] = {}
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
        resp_soup = BeautifulSoup(resp.text, "lxml")
        resp.close()

        tag_td_torrent = resp_soup.find_all("td", class_="torrent")
        tag_td_torrentdate = resp_soup.find_all("td", class_="torrentdate")
        tag_td_torrentdate = [f"{tag.text}".strip() for tag in tag_td_torrentdate]
        raw_data: list[RawDistroData] = list(
            zip(
                [f"{tag.text}".strip() for tag in tag_td_torrent[::2]],
                [
                    (
                        f"{tag.a.text}".strip(),
                        f"{TorrentArchiveScraper.START_URL}{tag.a['href']}".strip(),
                        date,
                    )
                    for tag, date in zip(tag_td_torrent[1::2], tag_td_torrentdate)
                ],
            )
        )

        for data in raw_data:
            if self.feed.get(data[0]) is None:
                self.feed[data[0]] = []
            self.feed[data[0]].append(
                {"name": data[1][0], "torrent_url": data[1][1], "date": data[1][2]}
            )
        # print(raw_data[:2], sep="\n")

    def get(self) -> dict[str, list[TorrentData]]:
        return self.feed


if __name__ == "__main__":
    from pprint import PrettyPrinter

    # NOTE: pipe the script output with something like `less`
    # since the output is going to be lengthy
    PrettyPrinter().pprint(TorrentArchiveScraper().feed)
