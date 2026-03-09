import requests
from datetime import datetime, UTC
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
document_to_index = {
    "location": "14.76, -14.76",
    "typeproduit": "electronique",
    "prix": 220,
    "agent_timestamp": datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
}

index_name = "index_name"

url = "https://host:9200/" + index_name + "/_doc"

headers = {'Content-Type': 'application/json'}

auth = ('admin', '')

response = requests.post(
    url,
    json=document_to_index,
    headers=headers,
    auth=auth,
    verify=False   # car certificat OpenSearch self-signed
)

print("Statut :", response.status_code)
print("Réponse :", response.text)
