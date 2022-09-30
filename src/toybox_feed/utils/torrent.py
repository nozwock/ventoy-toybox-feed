import urllib
from pathlib import Path

from torrentool.api import Torrent


def get_magnet_link(filepath: str | Path) -> str:
    torrent_file = Torrent.from_file(filepath)
    paramstr = urllib.parse.urlencode(  # type: ignore
        {
            "xt": torrent_file.magnet_link.split("?xt=")[-1],
            "dn": torrent_file.name,
            "tr": torrent_file.announce_urls,
            "ws": torrent_file.webseeds,
        }
    )
    return f"magnet:?{paramstr}"
