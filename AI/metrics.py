from prometheus_api_client import PrometheusConnect
from google.auth.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
#credentials = Credentials.from_service_account_file('/Users/ricardo/Documents/AI-GCP-BOT/tf-gke/AI/tf-ai-gke.json')
#credentials = service_account.Credentials.from_service_account_file(
   # 'tf-ai-gke.json')
KEY_FILE_LOCATION = 'tf-ai-gke.json'
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
creds = service_account.Credentials.from_service_account_file(
    KEY_FILE_LOCATION, scopes=SCOPES)

pc = PrometheusConnect(url='https://monitoring.googleapis.com/v1/projects/tf-ai-gke/location/global/prometheus/api/v1/', 
                       headers={'Authorization': 'Bearer ' + 'token.json'})
                       compute = build('compute', 'v1', credentials=creds)
zones = compute.zones().list(project='tf-ai-gket').execute()
print(zones)
# query = '100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)'                       
# data = pc.query(query)