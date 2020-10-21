# Ona Google Cloud Pipeline
Python pipeline for migrating API data into Google Cloud Storage and BigQuery


## Script

	load_local_csv_to_storage_to_bq

The script load_local_csv_to_storage_to_bq.py is a python script that loads a local csv file to a cloud storage bucket in a google cloud project. Then optionally it uses this bucket object as source and loads the csv to bigquery.

## Usage

The script takes the following parameters:
`-C file_path`
	 It is the file path of the consolidated json config file. Defaults to ~/asoba/bq_config.json.  Optional 
	 
`-D target dataset name `
	The name of the dataset where the csv file will be uploaded as a target table. If Big Query loading is not done then this argument is ignored. Required. 
	
`-F file path`
	It is the file path of the local csv file (with header) which is to be uploaded to the bucket and to biquery. Required
	
`-T tablename`
	It is the name of the target table in the dataset which will hold the csv data. It defaults to the extension less csv filename. Optional
	
`-W write_mode`
	It indicates whether the data is to be appended or the table should be truncated and reloaded. Defaults to whatever is in the config file. If absent there then defaults to WRITE_TRUNCATE. Optional
	
`-B bucket_name`
	This is the name of the bucket into which the csv file is first loaded. Required
	
`-M storage mode`
	Whether to load the bucket objecy as bigquery table. Optional. Values [ 'STORAGE_ONLY', 'BIGQUERY']. STORAGE_ONLY only uploads to cloud storage while as BIGQUERY first uploads to cloud storage and then to bug query.
	

## Setup and prerequisites

- Python 3 to be installed.
- google-cloud-bigquery python package to be installed.
- google-cloud-storage python packahe to be installed.
- python-dotenv should be installed
- `bq_config.json` file should be present. Sample provided in the bundle. Location can be different  but would need to be passed to the script at runtime with -C option.
- An env folder should be created somewhere on file system to hold the file containing environment variables. The reference to the environment file is in the config json file with the key user_env_file.
		It is used for credentials or anything else you may wish to expose as environment variable. Environment variables are inturn declared as 
		
	`SET variable_name=value e.g.`
	
	`SET GOOGLE_APPLICATION_CREDENTIALS=~/asoba/auth.json`
	

## Example:
	`python load_local_csv_to_storage_to_bq.py -D ingest_geographies -F ~/asoba/sql_runner_25zdqcrjpfsgdq_2020-08-11_07-39-17.csv -B ingest_geographies -M STORAGE_ONLY`

## Response:
json on successfull execution of the below format.

	`{"project": "asoba-241019", "storage_status": 0, "table_status": 1, "storage_mode": "STORAGE_ONLY", "source_csv": "~/asoba/sql_runner_28zdqcrjpfsgdq.csv", "storage": {"bucket": "ingest_geographies", "blob": "sql_runner_28zdqcrjpfsgdq.csv",  "blob_uri": "gs://ingest_geographies/sql_runner_28zdqcrjpfsgdq.csv"}}`

## Other usages and improvements:
In production mode can be run in a loop with csv, target table name and other parameters provided in a list.
response can be provided for exceptions to keep track of failed attempts instead of raising exceptions.

## Scheduling the script
The script load_local_csv_to_storage_to_bq.py is scheduled to get triggered whenever a new file "arrives" in the folder /home/master/shared_folder/export.
Linux incron tool is used to schedule the trigger. Arriving a file means a file is moved to the folder. Creating or editing an existing file in the folder WILL NOT trigger the execution of the script.

To create a new trigger/modify a trigger we use the command(per user):
incrontab -e

This opens incrontab entry for the currently logged in user.
Every line in the table is one trigger.
Every folder can have at max one trigger associated.
Incrontab is not time scheduled unlike cron which defines timed triggers. Here the design is "on an event of file arrival".

A sample of incrontab entry is as below:
/home/master/shared_folder/export IN_MOVED_TO sudo python3 /home/master/shared_folder/scripts/ona/bq/ona-google-cloud-pipeline/load_local_csv_to_storage_to_bq.py -D ingest_geographies -F $@/$# -B ingest_geographies -M BIGQUERY

The first part ie. /home/master/shared_folder/export indicates the folder which is to be observered.
The second part ie. IN_MOVED_TO defines the trigger event, which in our case is a file is moved to the said folder.
The rest of the command is the full command to execute with certain flags like $@ (folder) and $# (the file which is moved)

Any other folders can be set to monitor file arrival on the same principle provided right permissions are available for the user.
Also the file /etc/incron.allow should have the list of users(one per line) who are allowed to setup incron
