from prometheus_api_client import PrometheusConnect
from google.auth.credentials import Credentials

#credentials = Credentials.from_service_account_file('/Users/ricardo/Documents/AI-GCP-BOT/tf-gke/AI/tf-ai-gke.json')
credentials = service_account.Credentials.from_service_account_file(
    'tf-ai-gke.json')
credentials.apply()

pc = PrometheusConnect(url='https://monitoring.googleapis.com/v1/projects/tf-ai-gke/location/global/prometheus/api/v1/', 
                       headers={'Authorization': 'Bearer ' + 'token.json'})
