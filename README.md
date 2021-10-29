This repo contains scripts we use to scrape (with permission) data from different project's websites.



# BEACO2N

All BEACO2N data is provided by the [BEACO2N project](http://beacon.berkeley.edu/) at the University of Berkeley. Please make sure you get their permission before using any
of the scraping tools provided in this repository.

Below you can choose to either use the pipeline script which automates the download, processing and export of the data or perform each step yourself for greater control over the process.
For both steps you'll first need to retrieve the site metadata and optionally customise it to only include the sites you're interested in.

## Get site metadata

To retrieve BEACO2N data we first need to download the metadata file available on their website.
Get this from the link at the bottom of [http://beacon.berkeley.edu/metadata/](http://beacon.berkeley.edu/metadata/)
under "BEACO2N Locations". This should give you a file called `get_latest_nodes.csv`.

If you want to retrieve data for every site you can take this file and pass it to `metadata.py`. 

Usage:

``` bash
$ python metadata.py get_latest_nodes.csv
```

This will create a file called `get_latest_nodes_parsed.json` which contains just the information we need to retrieve
the data and some associated metadata (such at lat/long, masl etc).

If you only want to download data from a subset of the sites, modify the CSV to remove the sites you don't want and then follow the
steps above. 

> **_NOTE:_**  Remember to leave the headers if modifying the csv.

## Pipeline

The process of retrieving, processing and exporting the BEACO2N data can be performed in a single step with the `run_pipeline_beaco2n.py` script. We use this pipeline to perform automated updates of the BEACO2N data on the [OpenGHG data dashboard](https://openghg.github.io/dashboard/).

With the site metadata `csv` file to hand you can run

``` bash
$ python run_pipeline_beaco2n.py --vars co2 --export glasgow_co2_data.json --dir beaco2n/
```

You should now have a `glasgow_co2_data.json` file containing all the data required by the dashboard.

## Separate stages

To give you greater control over the process each of the scripts in the `beaco2n/beaco2n/` directory can be used to do each stage of the process separately. Each of the steps below expects the user to be in that `beaco2n/beaco2n/` directory. We also expect you to have followed the steps in the `Get site metadata` step above.

### Retrieve data

After creating the metadata `JSON` file above (see `Get site metadata`) you're ready to retrieve the data. This is done using the `scraper.py` file.
Say we removed all sites except for those in Glasgow and created a `sites_glasgow_parsed.json` in the step above, we now
run

``` bash
$ python scraper.py sites_glasgow_parsed.json
```

This will download the data from each of those sites from the date it was deployed to the current date.
A file will be created for each site in the format `{SITENAME}_{SITE_CODE}.csv`. These files can then be
processed using the OpenGHG `ObsSurface.read_file` function by passing it `data_type="BEACO2N"`.


## Process data

Now we have the data we can process it using OpenGHG, we just need the path to the data folder and the JSON metadata file we created in
the first step. Then we can do

``` bash
$ python process.py data/ glasgow_nodes_parsed.json 
```

And you should see something like

``` bash
[gareth@computer beaco2n]$ python process_beaco2n.py data/ glasgow_nodes_parsed.json 
INFO:numexpr.utils:NumExpr defaulting to 8 threads.
Processing: 174_HILLPARKSECONDARYSCHOOL.csv: 100%|████████████████████████| 1/1 [00:00<00:00, 13.39it/s]
Processing: 179_JOHNPAULACADEMY.csv: 100%|████████████████████████████████| 1/1 [00:00<00:00, 15.64it/s]
Processing: 178_STTHOMASAQUINASRCSECONDARYSCHOOL.csv: 100%|███████████████| 1/1 [00:00<00:00, 17.69it/s]
Processing: 193_KNIGHTSWOODSECONDARY.csv: 100%|███████████████████████████| 1/1 [00:00<00:00, 17.78it/s]
Processing: 171_UNIVERSITYOFSTRATHCLYDE.csv: 100%|████████████████████████| 1/1 [00:00<00:00, 56.90it/s]
Processing: 175_BELLAHOUSTONACADEMY.csv: 100%|████████████████████████████| 1/1 [00:00<00:00, 15.94it/s]
Processing: 156_KILLEARNSTIRLINGSHIREGLASGOWS22002.csv: 100%|█████████████| 1/1 [00:00<00:00, 12.97it/s]
Processing: 172_STPAULSHIGHSCHOOL.csv: 100%|██████████████████████████████| 1/1 [00:00<00:00,  7.44it/s]
Processing: 197_NOTREDAMEHIGHSCHOOL.csv: 100%|████████████████████████████| 1/1 [00:00<00:00, 12.87it/s]
Processing: 157_GLASGOWS12002.csv: 100%|██████████████████████████████████| 1/1 [00:00<00:00, 13.17it/s]
{'174_HILLPARKSECONDARYSCHOOL': defaultdict(<class 'dict'>, {'processed': {'174_HILLPARKSECONDARYSCHOOL.csv': {'pm': 'd3197540-09bf-40ef-b938-8a279aa5654e', 'co': '30400d37-998c-4587-ba03-b75d3aff9ad1', 'co2': '29bce2bd-1108-4730-981f-7245fc823701'}}}), '179_JOHNPAULACADEMY': defaultdict(<class 'dict'>, {'processed': {'179_JOHNPAULACADEMY.csv': {'pm': '40aa9e67-4de3-4485-86e3-44528a307b61', 'co': '985a6647-f59f-4d6e-8809-698e15d1fb6d', 'co2': '6d0a7d4c-a03d-4ade-911c-055cd4471ec6'}}}), '178_STTHOMASAQUINASRCSECONDARYSCHOOL': defaultdict(<class 'dict'>, {'processed': {'178_STTHOMASAQUINASRCSECONDARYSCHOOL.csv': {'pm': '503bf5f2-fdf6-46ba-99d6-fb4670795289', 'co': '1b4e3302-564c-4aa9-94e0-ef3ebaa96496', 'co2': '574a4922-5738-4963-821c-8711a37eac68'}}}), '193_KNIGHTSWOODSECONDARY': defaultdict(<class 'dict'>, {'processed': {'193_KNIGHTSWOODSECONDARY.csv': {'pm': '194be05a-7890-40b8-9eb7-2a437cf4c040', 'co': '4a7fb8d4-4eb4-43a4-a631-dc0e6442f672', 'co2': '2294d812-6da3-454f-8072-5e896c43e047'}}}), '171_UNIVERSITYOFSTRATHCLYDE': defaultdict(<class 'dict'>, {'processed': {'171_UNIVERSITYOFSTRATHCLYDE.csv': {}}}), '175_BELLAHOUSTONACADEMY': defaultdict(<class 'dict'>, {'processed': {'175_BELLAHOUSTONACADEMY.csv': {'pm': '6a4f83fc-596a-4dd2-89d0-3c4e28ac5e55', 'co': '9b1e2a15-1826-4bda-888e-236333a61f75', 'co2': '05c8e25a-648d-46a2-b571-2745eefdd670'}}}), '156_KILLEARNSTIRLINGSHIREGLASGOWS22002': defaultdict(<class 'dict'>, {'processed': {'156_KILLEARNSTIRLINGSHIREGLASGOWS22002.csv': {'pm': 'c0e67ddc-bd65-49b0-b959-beee6e7e27cf', 'co': '2b653fb5-4d0f-4d50-8647-0188c444896c', 'co2': 'd95c1ab1-1829-4155-9628-839af5ddb411'}}}), '172_STPAULSHIGHSCHOOL': defaultdict(<class 'dict'>, {'processed': {'172_STPAULSHIGHSCHOOL.csv': {'pm': '05c954a5-bf7d-4634-8ee9-ab9f83f7cbe3', 'co': '25c68766-42ab-4597-85c7-586dc456fa5a', 'co2': '17996dc2-68a7-434c-ace4-c941c94bcfe7'}}}), '197_NOTREDAMEHIGHSCHOOL': defaultdict(<class 'dict'>, {'processed': {'197_NOTREDAMEHIGHSCHOOL.csv': {'pm': '95708c61-1930-4917-9ab5-dd4307c8a82c', 'co': '84a48ac3-fd16-4299-83aa-1fc56a762964', 'co2': 'e3f37337-45ef-4326-986a-b55bfe402c8a'}}}), '157_GLASGOWS12002': defaultdict(<class 'dict'>, {'processed': {'157_GLASGOWS12002.csv': {'pm': '7fcce4fb-4eca-43bd-9610-ad13ab853bd5', 'co': '274a4d9b-e5fc-425e-b01c-459feb8b0000', 'co2': '77a401aa-ad11-474a-98a9-82c874a77717'}}})}
```

We've now process all the data we've retrieved from the BEACO2N site and the data is stored in the OpenGHG object store. The next step is to 
export it to a format the dashboard can read.

### Export data

Now we retrieve the data in a format that [the dashboard](https://github.com/openghg/dashboard) can read. We do this using the `retrieve_export.py` script. To use this script we use the `glasgow_nodes_parsed.json` file we created above, a list of the species we want from the data and an output filename.

``` bash
$ python retrieve_export.py glasgow_nodes_parsed.json co2 co pm --out glasgow_data.json
```

This then searches the object store for the sites given in `glasgow_nodes_parsed.json`, retrieves the data, processes it to a format
the dashboard can read and then exports it to a JSON file called `glasgow_data.json`.

The files `glasgow_nodes_parsed.json` and `glasgow_data.json` can then be placed in the dashboard [`data` directory](https://github.com/openghg/dashboard/tree/main/src/data). For updating the dashboard to use the new site data see the [dashboard README](https://github.com/openghg/dashboard/blob/main/README.md).


## AQMesh

### Pipeline

The process for `AQMesh` data is very similar to that for `BEACO2N`. We just need to run the `run_aqmesh_pipeline.py` script

``` bash
$ python run_pipeline_aqmesh.py --species co2 --vars co2 --export aqmesh_data.json --dir aqmesh/
```

This will download, process and export CO2 data from the AQMesh site to `aqmesh_data.json`. The retrieved data is stored in `aqmesh/`. 


## Combining network data

The dashboard can handle data from multiple networks. Using the `combine_networks` function from `webscrape.util` we can easily combine a number
of datasets. 

```bash
$ python combine_datasets.py --in beaco2n_data.json aqmesh_data.json --out combined_data.json
```

You should now have a `combined_data.json` file that can be imported by the dashboard. See instructions for updating the
dashboard with this new data file in the [dashboard documentation](https://github.com/openghg/dashboard#update-site-data-import).


## Glasgow Science Tower Picarro

This functionality doesn't quite belong in a repository called `webscrape` but fits with the updating of the data dashboard.
