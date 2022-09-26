<div align="center">
    <h1>Ventoy Toybox Feeds</h1>
</div>

<p align="center">
    This is the scraper component of the Ventoy Toybox application which is responsible for generating the required feeds for it
</p>

## Details

* Info such as Linux-distros torrent details are scraped from `distrowatch.com` currently.<br>
For e.g. this is how the scraped data is structured in a JSON format:-
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

# Developer Environment

> System Requirements > [Python](https://www.python.org/downloads/), [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/)

## Initializing virtual environment

Execute the following commands in the project root folder:

```sh
python -m venv .venv
```

Now, activate your virtual environment

```sh
# On Windows, run:
.venv\Scripts\activate.bat

# On nix systems, run:
source .venv/bin/activate
```

## Installing dependencies

Install all the required dependencies, via:

```sh
pip install .
# you could also use poetry
```

Now you can run the scraper by executing the following command:

```sh
python -m toybox_feed.cli
```