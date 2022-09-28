from torrentool.api import Torrent
from pathlib import Path
import urllib


def get_magnet_link(file_path: str | Path) -> str:
    torrent_file = Torrent.from_file(file_path)
    paramstr = urllib.parse.urlencode(
        {
            "xt": torrent_file.magnet_link.split("?xt=")[-1],
            "dn": torrent_file.name,
            "tr": torrent_file.announce_urls,
            "ws": torrent_file.webseeds,
        }
    )
    return f"magnet:?{paramstr}"
