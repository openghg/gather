This repo contains scripts we use to scrape (with permission) data from different project's websites.

## BEACO2N

### Get site metadata

To retrieve BEACO2N data we first need to download the metadata file available on their website.
Get this from the link at the bottom of [http://beacon.berkeley.edu/metadata/](http://beacon.berkeley.edu/metadata/)
under "BEACO2N Locations". This should give you a file called `get_latest_nodes.csv`.

If you want to retrieve data for every site you can take this file and pass it to `extract_site_data.py`. 

Usage:

``` bash
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

``` bash
$ python get_data.py sites_glasgow_parsed.json
```

This will download the data from each of those sites from the date it was deployed to the current date.
A file will be created for each site in the format `{SITENAME}_{SITE_CODE}.csv`. These files can then be
processed using the OpenGHG `ObsSurface.read_file` function by passing it `data_type="BEACO2N"`.


## Process data

Now we have the data we can process it using OpenGHG, we just need the path to the data folder and the JSON metadata file we created in
the first step. Then we can do

``` bash
$ python process_beaco2n.py data/ glasgow_nodes_parsed.json 
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

### Export to dashboard


