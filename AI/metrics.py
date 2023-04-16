import os
import requests
from prometheus_api_client import PrometheusConnect
from google.auth.credentials import Credentials
from google.oauth2 import service_account
import prometheus_api_client
import json


KEY_FILE_LOCATION = 'tf-ai-gke.json'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
creds = service_account.Credentials.from_service_account_file(
    KEY_FILE_LOCATION, scopes=SCOPES)

prom = PrometheusConnect(url ="http://localhost:9090", disable_ssl=True)
 


#Query 1  This query calculates the average percentage of CPU utilization across all instances 
#by subtracting the average percentage of time that the CPU is idle from 100
query1 = '100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)'
result1 = prom.custom_query(query1)
json_string = json.dumps(result1).replace("'",'"')
json_data = json.loads(json_string)
instances_and_values = list(map(lambda x: (x['metric']['instance'], x['value'][1]), json_data))
jsonF= json.dumps(instances_and_values).replace("'",'"')
print("average percentage of CPU utilization across all instances: "+"\n"+jsonF+"\n")

#Query 2 calculates the per-second CPU usage across all non-idle CPU modes (such as user, system, iowait) 
#for each Kubernetes node in the cluster over the last 5 minutes.
query2= 'sum by (kubernetes_node) (rate(node_cpu_seconds_total{mode!="idle"}[5m]))'
result2 = prom.custom_query(query2)
json_string2 = json.dumps(result2).replace("'",'"')
json_data2 = json.loads(json_string2)

instances_and_values2 = list(map(lambda x: x['value'][1], json_data))
jsonF2= json.dumps(instances_and_values2).replace("'",'"')
print("calculates the per-second CPU usage across all non-idle CPU modes (such as user, system, iowait)"+"\n"
+jsonF2+"\n")


#Query 3 
query3= 'sum by (instance) (irate(node_memory_Active_bytes[1m])) / count by (instance) (node_memory_MemTotal_bytes)'
result3 = prom.custom_query(query3)
json_string3 = json.dumps(result3).replace("'",'"')
json_data3 = json.loads(json_string3)

instances_and_values3 = list(map(lambda x: (x['metric']['instance'], x['value'][1]), json_data))
jsonF3= json.dumps(instances_and_values3).replace("'",'"')
print("this metric gets the per-second memory usage in each node: "+"\n"+jsonF3)