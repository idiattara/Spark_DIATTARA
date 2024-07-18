import requests
from datetime import datetime

# Document JSON à indexer
document_to_index = {
    "location": "14.76, -14.76",
    "typeproduit": "electronique",
    "prix": 220,
    "agent_timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
}

# Nom de l'index
index_name = "index_name"  

# URL Elasticsearch avec authentification basique
url = "http://hostname:9200/" + index_name + "/_doc"

# Headers JSON
headers = {'Content-Type': 'application/json'}

# Authentification Elasticsearch (elastic / changeme)
auth = ('user', 'password')

# Indexation du document
response = requests.post(url, json=document_to_index, headers=headers, auth=auth)
response.raise_for_status()

# Affichage du statut de la requête et de la réponse
print("Statut de la requête:", response.status_code)
print("Réponse de Elasticsearch:", response.text)
