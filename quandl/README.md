# Quandl Google Cloud Pipeline
Python pipeline for migrating API data from Quandl into Google Cloud Storage and BigQuery

## SCRIPT
        process_quandl_ds.py
PURPOSE
The script process_quandl_ds.py is the python script that access quandl.com api data exposed via https and then optionally it loads to bucket and to bigquery.

## USAGE
The script takes the following parameters:
`-C file_path`
         It is the file path of the consolidated json config file. Defaults to /home/master/shared_folder/scripts/ona/bq/ona-google-cloud-pipeline/bq_config.json.  Optional

`-D source dataset name `
        The name of the dataset in quandl.com whose the csv file will be downloaded locally and then optionally, uploaded as a target table into Big Query loading is not done then this argument is ignored. Required.
		The target table name in BigQuery is always UMICH_<dataset name> e.g. UMICH_SOC43. Also stored with same name in google cloud (with csv extension)
`-L directory path`
        It is the directory path of the local csv file (with header) where csv file shall be downloaded to. Defaults to /home/master/shared_folder/import/UMICH. Optional

`-U Upload flag`
        If not none, then the downloaded csv file will be uploaded to bigquery. If not specified only csv file will be downloaded and shall not be uploaded to bigquery


## SETUP AND PREREQUISITES

- Python 3 to be installed.
- google-cloud-bigquery python package to be installed.
- google-cloud-storage python packahe to be installed.
- python-dotenv should be installed
- requests, json, csv packages installed.
- the ona generic upload script at /home/master/shared_folder/scripts/ona/bq/ona-google-cloud-pipeline/load_local_csv_to_storage_to_bq.py is required ( and all its dependencies) to do the actual upload part.

## SAMPLE RUN:
	python3 process_quandl_ds.py -D SOC43 -U Yes

## CONFIGURATION SETTINGS:
	The env file should contain the QUANDL_API_KEY holding the api key. The location of env file is /home/master/shared_folder/scripts/ona/bq/env/bq_pipeline.env
	The config file /home/master/shared_folder/scripts/ona/bq/ona-google-cloud-pipeline/bq_config.json should contain the default bucket name and default dataset name in the json
	
## OTHER SETTINGS:
	Incrontab entries shall not be executed unless set up. The script however can do the full upload provided flags are provided at runtime.

