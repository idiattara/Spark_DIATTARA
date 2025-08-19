import requests
import json

# URL du cluster Elasticsearch
BASE_URL = "http://clustersdaelatsic.eastus.cloudapp.azure.com:9200"

# Authentification
AUTH = ("your user", "you passeword")
HEADERS = {"Content-Type": "application/json"}

# Corps de la requête PUT (mapping)
template_payload = {
    "index_patterns": ["your patern*"],
    "template": {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 2
        },
        "mappings": {
            "properties": {
                "location": {
                    "type": "geo_point"
                },
                "prix": {
                    "type": "long"
                },
                "typeproduit": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "agent_timestamp": {
                    "type": "date",
                    "format": "yyyy-MM-dd_HHmmss||strict_date_time||strict_date_optional_time||epoch_millis||strict_date_optional_time_nanos"
                }
            }
        }
    }
}

# Requête PUT vers Elasticsearch
resp = requests.put(
    f"{BASE_URL}/_index_template/template_yourpattern",
    headers=HEADERS,
    auth=AUTH,
    data=json.dumps(template_payload)
)

print("Statut:", resp.status_code)
print("Réponse:", resp.text)
