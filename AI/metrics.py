import os
import requests
from prometheus_api_client import PrometheusConnect
from prometheus_api_client.utils import parse_datetime
from datetime import timedelta
from google.auth.credentials import Credentials
from google.oauth2 import service_account
import prometheus_api_client
import tensorflow as tf
import subprocess
import json

#terraform directory
terraform_dir = '/Users/ricardo/Documents/AI-GCP-BOT/tf-gke/terraform'
# set the thresholds for applying the appropriate .tfvars file
high_threshold = 0.80
low_threshold = 4604.6855
#project info
project_id = "tf-ai-gke"
region = "us-central1"

# configure the credentials for accessing GKE clusters
KEY_FILE_LOCATION = 'tf-ai-gke.json'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
creds = service_account.Credentials.from_service_account_file(
    KEY_FILE_LOCATION, scopes=SCOPES)
# connect to Prometheus and retrieve the metrics
prom = PrometheusConnect(url ="http://localhost:9090", disable_ssl=True)

# Set the Prometheus query range and resolution
#query_range = "1h"
#query_resolution = "1m"
start_time = parse_datetime("6h")
end_time = parse_datetime("now")
step = 60
#start_time,end_time,step
#Query 1  This query calculates the average percentage of CPU utilization across all instances 
#by subtracting the average percentage of time that the CPU is idle from 100
# Query 1 - CPU utilization across all instances
query1 = '100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)'
result1 = prom.custom_query(query1)
json_string = json.dumps(result1).replace("'",'"')
json_data = json.loads(json_string)
instances_and_values1 = list(map(lambda x: (x['metric']['instance'], x['value'][1]), json_data))
jsonF= json.dumps(instances_and_values1).replace("'",'"')
#jsonF= json.dumps(json_data).replace("'",'"')
print("average percentage of CPU utilization across all instances: "+"\n"+jsonF+"\n")

#Query 2 calculates the per-second CPU usage across all non-idle CPU modes (such as user, system, iowait) 
#for each Kubernetes node in the cluster over the last 5 minutes.
query2= 'sum by (kubernetes_node) (rate(node_cpu_seconds_total{mode!="idle"}[5m]))'
result2 = prom.custom_query(query2)
json_string2 = json.dumps(result2).replace("'",'"')
json_data2 = json.loads(json_string2)
instances_and_values2 = list(map(lambda x: x['value'][1], json_data2))

jsonF2= json.dumps(instances_and_values2).replace("'",'"')
print("calculates the per-second CPU usage across all non-idle CPU modes (such as user, system, iowait)"+"\n"+jsonF2+"\n")



#Query 3 
query3= 'sum by (instance) (irate(node_memory_Active_bytes[1m])) / count by (instance) (node_memory_MemTotal_bytes)'
result3 = prom.custom_query(query3)
json_string3 = json.dumps(result3).replace("'",'"')
json_data3 = json.loads(json_string3)
instances_and_values3 = list(map(lambda x: (x['metric']['instance'], x['value'][1]), json_data3))

jsonF3= json.dumps(instances_and_values3).replace("'",'"')
print("this metric gets the per-second memory usage in each node: "+"\n"+jsonF3)

# combine the metrics into a format that can be used for training the model
metrics = []
for i in range(len(instances_and_values1)):
    instance, value1 = instances_and_values1[i]
    value2 = instances_and_values2[0]
    instance, value3 = instances_and_values3[i]
    metrics.append((float(value1), float(value2), float(value3)))
    print(metrics)
# Define the variables that cannot be changed by the metrics
query1_weight = 0.8
query2_weight = 0.1
query3_weight = 0.1

# Compute the weighted average of the metrics and make the deployment decision
avg_metric = tf.reduce_sum(tf.multiply(metrics, [query1_weight, query2_weight, query3_weight]), axis=1)
print(avg_metric)
if tf.reduce_any(avg_metric <= low_threshold):
    # apply the low-use .tfvars file
    tfvars_file2 = 'variables-sgkenode.tfvars'
    cmd2 = f"terraform apply -var-file={terraform_dir}/variables-sgkenode.tfvars"
    subprocess.run(cmd2, shell=True, cwd=terraform_dir)
    print(f'The average metric value is {avg_metric}. Applying {tfvars_file2}')


elif  tf.reduce_all(avg_metric >= high_threshold):
    # apply the high-use .tfvars file
    tfvars_file = 'variables-bgkenode.tfvars'
    cmd = f"terraform apply -var-file={terraform_dir}/variables-bgkenode.tfvars"
    subprocess.run(cmd, shell=True, cwd=terraform_dir)
    print(f'The average metric value is {avg_metric}. Applying {tfvars_file}')
else:
    # apply the default .tfvars file
    tfvars_file3 = 'variables-mgkenode.tfvars'
    cmd3 = f"terraform apply -var-file={terraform_dir}/variables-mgkenode.tfvars"
    subprocess.run(cmd3, shell=True, cwd=terraform_dir)
    print(f'The average metric value is {avg_metric}. Applying {tfvars_file3}')