<div align="center">
    <h1>Ventoy Toybox Feeds</h1>
</div>

<p align="center">
    This is the scraper component of the Ventoy Toybox application which is responsible for generating the required feeds for it
</p>

<div align="center">

[![Scrape](https://github.com/nozwock/ventoy-toybox-feed/actions/workflows/ci.yml/badge.svg)](https://github.com/nozwock/ventoy-toybox-feed/actions/workflows/ci.yml)

</div>

## Links

-   JSON:

```
https://github.com/nozwock/ventoy-toybox-feed/releases/download/feeds/releases.json
```

## Details

-   Data such as Linux-distros torrent details are scraped from `distrowatch.com` currently.<br>
    Structure of parsed JSON:-

```json
[
    {
        "group": "KDE neon",
        "name": "neon-user-20220908-0946.iso.torrent",
        "torrent_url": "https://www.distrowatch.com/dwres/torrents/neon-user-20220908-0946.iso.torrent",
        "date": "2022-09-08",
        "magnet": "magnet:?xt=urn:btih:0354be1c567ff84067ad2cfaacdf911583a6b9e8&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&ws=https%3A%2F%2Ffiles.kde.org%2Fneon%2Fimages%2Fuser%2F20220908-0946%2Fneon-user-20220908-0946.iso"
    },
    {
        "group": "Raspberry Pi OS",
        "name": "raspios-2022-09-06-raspios-bullseye-armhf.img.xz.torrent",
        "torrent_url": "https://www.distrowatch.com/dwres/torrents/raspios-2022-09-06-raspios-bullseye-armhf.img.xz.torrent",
        "date": "2022-09-07",
        "magnet": "magnet:?xt=urn:btih:02535d5bbb346e201fa120d0c1411f0e591b5291&tr=http%3A%2F%2Ftracker.raspberrypi.org%3A6969%2Fannounce"
    },
    ...
]
```
