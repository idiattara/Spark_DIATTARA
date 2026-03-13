from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime, UTC
import json
import tempfile
import os

PROJECT_ID = "diattara-490108"
TABLE_ID = "mosefdata.streamingsell"
KEY_PATH = "/content/diattara-490108-8c54f63e4b8b.json"

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

rows_to_insert = [
    {
        "location": "14.76, -14.76",
        "prix": 10.5,
        "typeproduit": "fruit",
        "agent_timestamp": datetime.now(UTC).isoformat()
    },
    {
        "location": "10.76, -14.76",
        "prix": 20.75,
        "typeproduit": "legume",
        "agent_timestamp": datetime.now(UTC).isoformat()
    }
]

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND
)

tmp_file = None

try:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        tmp_file = f.name
        for row in rows_to_insert:
            f.write(json.dumps(row) + "\n")

    with open(tmp_file, "rb") as source_file:
        job = client.load_table_from_file(
            source_file,
            TABLE_ID,
            job_config=job_config
        )

    job.result()
    print("Chargement réussi dans BigQuery")

except Exception as e:
    print("Erreur :", repr(e))

finally:
    if tmp_file and os.path.exists(tmp_file):
        os.remove(tmp_file)
