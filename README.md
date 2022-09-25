<div align="center">
    <h1>Ventoy Toybox Feeds</h1>
</div>

<p align="center">
    This is the scraper component of the Ventoy Toybox application which is responsible for generating the required feeds for it
</p>

## Details

* Info such as Linux-distros torrent details are scraped from `distrowatch.com` currently.<br>
for e.g. this is how the scraped data is structured in a JSON format:-
```json
{
    ...
    "EndeavourOS": [
        {
            "date": "2022-06-24",
            "name": "EndeavourOS_Artemis-22_6.iso.torrent",
            "torrent_url": "https://www.distrowatch.com/dwres/torrents/EndeavourOS_Artemis-22_6.iso.torrent"
        },
        {
            "date": "2022-04-08",
            "name": "EndeavourOS-Apollo-22_1.iso.torrent",
            "torrent_url": "https://www.distrowatch.com/dwres/torrents/EndeavourOS-Apollo-22_1.iso.torrent"
        },
        ...
    ]
    ...
}
```