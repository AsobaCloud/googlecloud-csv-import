# Ona Google Cloud Pipeline
Python pipeline for migrating API data into Google Cloud Storage and BigQuery


## SCRIPT
	load_local_csv_to_storage_to_bq
PURPOSE
The script load_local_csv_to_storage_to_bq.py is the python script that loads a local csv file to a cloud storage bucket in a google cloud project. Then optionally it uses this bucket object as source and loads the csv to bigquery.

## USAGE
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
	

## SETUP AND PREREQUISITES

- Python 3 to be installed.
- google-cloud-bigquery python package to be installed.
- google-cloud-storage python packahe to be installed.
- python-dotenv should be installed
- `bq_config.json` file should be present. Sample provided in the bundle. Location can be different  but would need to be passed to the script at runtime with -C option.
- An env folder should be created somewhere on file system to hold the file containing environment variables. The reference to the environment file is in the config json file with the key user_env_file.
		It is used for credentials or anything else you may wish to expose as environment variable. Environment variables are inturn declared as 
		
	`SET variable_name=value e.g.`
	`SET GOOGLE_APPLICATION_CREDENTIALS=C:/asoba/auth.json`
	

## SAMPLE RUN:
	`python load_local_csv_to_storage_to_bq.py -D ingest_geographies -F ~/asoba/sql_runner_25zdqcrjpfsgdq_2020-08-11_07-39-17.csv -B ingest_geographies -M STORAGE_ONLY`

## RESPONSE:
json on successfull execution of the below format.

	`{"project": "asoba-241019", "storage_status": 0, "table_status": 1, "storage_mode": "STORAGE_ONLY", "source_csv": "~/asoba/sql_runner_28zdqcrjpfsgdq.csv", "storage": {"bucket": "ingest_geographies", "blob": "sql_runner_28zdqcrjpfsgdq.csv",  "blob_uri": "gs://ingest_geographies/sql_runner_28zdqcrjpfsgdq.csv"}}`

## OTHER USAGES AND IMPROVEMENTS:
In production mode can be run in a loop with csv, target table name and other parameters provided in a list.
response can be provided for exceptions to keep track of failed attempts instead of raising exceptions.


