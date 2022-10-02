<div align="center">
    <h1>Ventoy Toybox Feeds</h1>
</div>

<p align="center">
    This is the scraper component of the Ventoy Toybox application which is responsible for generating the required feeds for it
</p>

## Links

- JSON:

```
https://github.com/nozwock/ventoy-toybox-feed/releases/download/feeds/releases.json
```

## Details

* Info such as Linux-distros torrent details are scraped from `distrowatch.com` currently.<br>
For e.g. this is how the scraped data is structured in a JSON format:-
```json
{
    ...
    "Debian": [
        {
            "name": "debian-11.4.0-amd64-DVD-1.iso.torrent",
            "torrent_url": "https://www.distrowatch.com/dwres/torrents/debian-11.4.0-amd64-DVD-1.iso.torrent",
            "date": "2022-07-09",
            "magnet": "magnet:?xt=urn:btih:7949ef20a89feb1a2838e5b1ef42676a2ae602cc&tr=http%3A%2F%2Fbttracker.debian.org%3A6969%2Fannounce"
        },
        {
            "name": "debian-live-11.2.0-amd64-kde.iso.torrent",
            "torrent_url": "https://www.distrowatch.com/dwres/torrents/debian-live-11.2.0-amd64-kde.iso.torrent",
            "date": "2021-12-26",
            "magnet": "magnet:?xt=urn:btih:9e1ce66d25276fc04e0e0ed7eef2cb671d0773af&tr=http%3A%2F%2Fbttracker.debian.org%3A6969%2Fannounce"
        },
        ...
    ],
    ...
}
```
