from azureml.core import Workspace, Dataset, Datastore
import pandas as pd
import os
from azureml.core.authentication import InteractiveLoginAuthentication
import argparse
import warnings
warnings.filterwarnings('ignore')

#-----------------------------XX-----------------------------------#

interactive_auth = InteractiveLoginAuthentication(tenant_id="tenant-id", force=True)

ws = Workspace(subscription_id= "subscription_id",
    resource_group= "mlops-demo",
    workspace_name= "mlops-demo", auth = interactive_auth) 
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')

#Name of blob datastore
data_store_name = 'workspaceblobstore'
#Name of Azure blob container 
container_name = os.getenv("BLOB_CONTAINER", "blob1238115514") 
#Name of Storage Account
account_name = os.getenv("BLOB_ACCOUNTNAME", "blob1238115514")


parser = argparse.ArgumentParser()
parser.add_argument("--input-data", type=str)
args = parser.parse_args()

datastore = Datastore.get(ws, 'workspaceblobstore')

from azureml.core import Run
run = Run.get_context()

#-----------------------------XX-----------------------------------#
#Read csv file
df = Dataset.Tabular.from_delimited_files(path=[(datastore, args.input_data)]).to_pandas_dataframe()
print("Shape of Dataframe", df.shape)

#-----------------------------XX-----------------------------------#
#Exporting the file
path = "tmp/"
try:
    os.mkdir(path)
except OSError:
    print("Creation of directory %s failed" % path)
else:
    print("Sucessfully created the directory %s " % path)
    
temp_path = path + "wranggled.csv"
df.to_csv(temp_path)

# to datastore
datastr = Datastore.get(ws, "workspaceblobstore")
datastr.upload(src_dir = path, target_path="", overwrite=True)
#-----------------------------XX-----------------------------------#
print("Completed Wrangling Process!")