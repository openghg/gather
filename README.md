This repo contains scripts we use to scrape (with permission) data from different project's websites.

## BEACO2N

### Get site metadata

To retrieve BEACO2N data we first need to download the metadata file available on their website.
Get this from the link at the bottom of [http://beacon.berkeley.edu/metadata/](http://beacon.berkeley.edu/metadata/)
under "BEACO2N Locations". This should give you a file called `get_latest_nodes.csv`.

If you want to retrieve data for every site you can take this file and pass it to `extract_site_data.py`. 

Usage:

```
$ python extract_site_data.py get_latest_nodes.csv
```

This will create a file called `get_latest_nodes_parsed.json` which contains just the information we need to retrieve
the data and some associated metadata (such at lat/long, masl etc).

If you only want to download data from a subset of the sites, modify the CSV to remove the sites you don't want and then follow the
steps above. 

> **_NOTE:_**  Remember to leave the headers if modifying the csv.


### Retrieve data

After creating the `json` file above you're ready to retrieve the data. This is done using the `get_data.py` file.
Say we removed all sites except for those in Glasgow and created a `sites_glasgow_parsed.json` in the step above, we now
run

```
$ python get_data.py sites_glasgow_parsed.json
```

This will download the data from each of those sites from the date it was deployed to the current date.
A file will be created for each site in the format `{SITENAME}_{SITE_CODE}.csv`. These files can then be
processed using the OpenGHG `ObsSurface.read_file` function by passing it `data_type="BEACO2N"`.
