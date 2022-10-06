<div align="center">
    <h1>Ventoy Toybox Feeds</h1>
</div>

<p align="center">
    This is the scraper component of the Ventoy Toybox application which is responsible for generating the required feeds for it
</p>

<div align="center">

[![Scrape](https://github.com/nozwock/ventoy-toybox-feed/actions/workflows/ci.yml/badge.svg)](https://github.com/nozwock/ventoy-toybox-feed/actions/workflows/ci.yml)

</div>


## Details

- Github's Action cronjob will run the script and upload the feeds to the [Releases] once a day.
- In case distrowatch.com goes down or scraping fails, check out last working feeds at [Releases].


## Links

- JSON:

```
https://github.com/nozwock/ventoy-toybox-feed/releases/download/feeds/releases.json
```

[releases]: https://github.com/nozwock/ventoy-toybox-feed/releases/tag/feeds