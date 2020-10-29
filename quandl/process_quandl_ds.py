import logging
from datetime import *
import argparse
import csv
from dotenv import load_dotenv
import os
import json
import requests

base_url = 'https://www.quandl.com/api/v3/datasets/UMICH/'
dataset_id='SOC43'
CONFIG_FILE='/home/master/shared_folder/scripts/ona/bq/ona-google-cloud-pipeline/bq_config.json'
QUANDL_DATA_SET='ingest_explore'
QUANDL_BUCKET='ingest_explore'

logging.basicConfig(filename="/home/master/shared_folder/logs/ona/bq/ona-google-cloud-pipeline_quandl_"+datetime.now().strftime('%Y_%m_%d')+".log",format='%(asctime)s %(message)s',filemode='a')

#Creating an object
logger=logging.getLogger()

#Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

#Argument Processing
ap = argparse.ArgumentParser()
ap.add_argument("-D", "--DATASET", required=True, help="Name of Dataset to download from Quandl")
ap.add_argument("-L", "--LOCATION", required=False, help="Local Directory to store csv to.")
ap.add_argument("-C", "--CONFIG_FILE", required=False, help="Optional config file.")
ap.add_argument("-U", "--UPLOAD", required=False, help="Upload to BIGQUERY.")

args = vars(ap.parse_args())
logger.info('Reading Configuration.....')
dataset_id=args['DATASET']
if args['LOCATION']:
    local_folder_to_store=args['LOCATION']
else:
    local_folder_to_store = '/home/master/shared_folder/import/UMICH'

if args['CONFIG_FILE']:
    config_file=args['CONFIG_FILE']
else:
    config_file = CONFIG_FILE
if args['UPLOAD']:
    upload_to_bq=True
else:
    upload_to_bq=False


if not os.path.exists(config_file):
    logger.warning('The config file ['+ config_file +']providing authentication info and project name could not be found. Will exit.')
    raise Exception("The config file providing authentication info and project name could not be found.")

with open(config_file, "r") as f:
    config_dict = json.load(f)

if config_dict.get("user_env_file"):
        user_env_file=config_dict.get("user_env_file")
else:
        user_env_file = "home/master/shared_folder/scripts/ona/bq/env/bq_pipeline.env"
load_dotenv(user_env_file)
api_key = os.getenv("QUANDL_API_KEY")
quandl_data_set =  QUANDL_BUCKET if  config_dict.get("quandl_bq_dataset") is None else config_dict.get("quandl_bq_dataset")
quandl_bucket = QUANDL_BUCKET if config_dict.get("quandl_bucket") is None else config_dict.get("quandl_bucket")
#print(quandl_data_set,quandl_bucket)

local_base_file_name='UMICH'+'_'+dataset_id + '.csv'
local_file_name = local_folder_to_store + '/' + local_base_file_name
#print(api_key)
data_url=base_url + dataset_id + '.csv?' + 'api_key=' + api_key

logger.info('Downloading dataset ' + dataset_id + ' from quandl.com.')
data=requests.get(data_url)
with open(local_file_name, 'wb') as f:
    for line in data:
        f.write(line)
logger.info('Saved dataset: ' + dataset_id + ' to local file ' + local_file_name)
if upload_to_bq:
    logger.info('Uploading dataset ' + dataset_id + ' to cloud and bigquery.')
    os.system(f"python3 /home/master/shared_folder/scripts/ona/bq/ona-google-cloud-pipeline/load_local_csv_to_storage_to_bq.py -C {config_file} -D {quandl_data_set} -F {local_file_name} -T UMICH_{dataset_id} -W WRITE_TRUNCATE -B {quandl_bucket} -M BIGQUERY")
    logger.info(f"Final upload to BQ done for dataset: {dataset_id}--> bq dataset: UMICH_{dataset_id}")
if os.path.exists(local_file_name):
    #os.remove(local_file_name)
    logger.info(f"Saved local file: {local_file_name}. ")
else:
  logger.warn("The file could not be downloaded.")
