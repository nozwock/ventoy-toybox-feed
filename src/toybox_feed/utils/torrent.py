from pathlib import Path

from torrentool.api import Torrent


def get_magnet_link(filepath: str | Path) -> str | None:
    torrent_file = Torrent.from_file(filepath)

    try:
        return str(torrent_file.get_magnet(detailed=True))
    except:
        return None

    # OLD -> will remove in future commits
    # paramstr = urllib.parse.urlencode(  # type: ignore
    #     {
    #         "xt": torrent_file.magnet_link.split("?xt=")[-1],
    #         "dn": torrent_file.name,
    #         "tr": torrent_file.announce_urls,
    #         "ws": torrent_file.webseeds,
    #     }
    # )
    # return f"magnet:?{paramstr}"
