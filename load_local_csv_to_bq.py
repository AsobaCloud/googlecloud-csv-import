from google.cloud import bigquery
import json
import os
import argparse
import re
from dotenv import load_dotenv
import logging
from datetime import *

#Set default values if any
DEFAULT_CONFIG_FILE = '/home/master/shared_folder/scripts/ona/bq/ona-google-cloud-pipeline/bq_config.json'

#Create and configure logger
logging.basicConfig(filename="/home/master/shared_folder/logs/ona/bq/ona-google-cloud-pipeline_"+datetime.now().strftime('%Y_%m_%d')+".log",format='%(asctime)s %(message)s',filemode='a')

#Creating an object
logger=logging.getLogger()

#Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)



#Argument Processing
ap = argparse.ArgumentParser()
ap.add_argument("-C", "--CONFIG_FILE", required=False, help="Config file location")
ap.add_argument("-D", "--TARGET_DATASET", required=True, help="Target Dataset to where the csv file will be loaded")
ap.add_argument("-F", "--SOURCE_CSV", required=True, help="Path of CSV to be loaded into the dataset")
ap.add_argument("-T", "--TARGET_TABLENAME", required=False, help="Name of table in the target dataset")
ap.add_argument("-W", "--WRITE_DISPOSITION", required=False, choices=['WRITE_TRUNCATE', 'WRITE_EMPTY', 'WRITE_APPEND'], help="Write Disposition ie. specifies if target table is to be overwritten or appended.")
args = vars(ap.parse_args())

# Mandatory variables
source_csv=args['SOURCE_CSV']
target_dataset=args['TARGET_DATASET']

#set variables and check file existence
if args['CONFIG_FILE']:
	config_file = args['CONFIG_FILE'] 
else:
	config_file = DEFAULT_CONFIG_FILE
if not os.path.exists(config_file):
        logger.warning('The config file ['+ config_file +']providing authentication info and project name could not be found. Will exit.')
        raise Exception("The config file providing authentication info and project name could not be found.")
if not os.path.exists(source_csv):
        logger.warning('The Source CSV file ['+source_csv+'] to be uploaded could not be found. Will exit.')
        raise Exception("The Source CSV file to be uploaded could not be found.")
if args['TARGET_TABLENAME']:
	target_tablename = args['TARGET_TABLENAME']
else:
	base=os.path.basename(source_csv)
	target_tablename = os.path.splitext(base)[0]
	target_tablename = re.sub('[^0-9a-zA-Z]+', '_', target_tablename)


# read default variables
with open(config_file, "r") as f:
    config_dict = json.load(f)
project=config_dict["project"]
if not args['WRITE_DISPOSITION']:
	if config_dict.get("write_disposition"):
		write_disposition=config_dict["write_disposition"]
	else:
		write_disposition="WRITE_TRUNCATE" #WRITE_EMPTY, WRITE_APPEND other possible values
else:
	write_disposition = args['WRITE_DISPOSITION']
if config_dict.get("user_env_file"):
	user_env_file=config_dict.get("user_env_file")
else:
	user_env_file = "/home/master/shared_folder/scripts/ona/bq/env/bq_pipeline.env"
load_dotenv(user_env_file)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# API Access to datasets. Dataset should already exist in the project.
client = bigquery.Client()
datasets = list(client.list_datasets())
dataset_names=[dataset.dataset_id for dataset in datasets]


if target_dataset not in dataset_names:
        logger.warning('Target dataset ['+target_dataset+'] not found in the project. Will exit.')
        raise Exception("Target dataset not in the project. Aborting.")

# Debug
# Start Load
logger.info("Starting upload of file ["+source_csv +"] to project [" + project + "] and dataset ["+ target_dataset +"]")
table_id = project + '.' + target_dataset + '.' + target_tablename
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True, quote_character='"',field_delimiter=";",write_disposition=write_disposition,
)
job_config.write_disposition = write_disposition
with open(source_csv, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)

# Wait for result
job.result()

# Send back response.
table = client.get_table(table_id)
response={'status':0, 'source_csv':source_csv, 'target_dataset':target_dataset, 'target_table':target_tablename, 'project':project, 'table': {'table_id':table_id, 'row_count_final':table.num_rows, 'column_count':len(table.schema)}, 'mode': write_disposition}
logger.info(json.dumps(response))
print(json.dumps(response))
logger.info("Process Ended")
