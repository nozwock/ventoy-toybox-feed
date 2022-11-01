from pathlib import Path

from torrentool.api import Torrent


def get_magnet_link(filepath: str | Path) -> str | None:
    torrent_file = Torrent.from_file(filepath)

    try:
        return str(torrent_file.get_magnet(detailed=True))
    except:
        return None
