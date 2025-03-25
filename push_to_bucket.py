#pip install google-cloud-storage

from google.cloud import storage
import json
from datetime import datetime

# Remplacez ceci par le chemin vers votre fichier de clé de service JSON
service_account_json = 'chemin_vers_votre_json_key'

# Créez un client de stockage Google Cloud
client = storage.Client.from_service_account_json(service_account_json, project='id_de_votre_projet')

# Nom du bucket et du répertoire
bucket_name = 'nom_de_votre_bucket'
directory_name = 'datasorbonne/'

# Créer le contenu JSON à uploader
data = [
    {"typeProduit":"Laitier","price":3826.4,"location":"3.7038, 8.4168"},
    {"typeProduit":"Electronics","price":12,"location":"7.4, 6"}
]

# Convertir le dictionnaire Python en format NEWLINE_DELIMITED_JSON (NDJSON)
ndjson_data = '\n'.join([json.dumps(item) for item in data])

# Nom du fichier dans le bucket (vous pouvez choisir un nom de fichier ici)
file_name = datetime.now().strftime('data_%Y%m%d_%H%M%S.json')

# Accéder au bucket
bucket = client.get_bucket(bucket_name)

# Définir le chemin complet du fichier dans le répertoire (datasorbonne)
blob = bucket.blob(directory_name + file_name)

# Upload du fichier JSON dans le bucket avec le format NEWLINE_DELIMITED_JSON
blob.upload_from_string(ndjson_data, content_type='application/json')

print(f"Fichier JSON téléchargé dans {bucket_name}/{directory_name}{file_name}")
