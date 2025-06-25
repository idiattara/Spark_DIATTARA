from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from datetime import datetime
import os

# Fonction pour lire un fichier CSV et renvoyer le chemin du fichier Parquet via XCom
def read_csv(**kwargs):
    spark = SparkSession.builder \
        .appName("Airflow PySpark CSV Read Example") \
        .getOrCreate()

    # Définir le chemin du fichier CSV
    input_csv = '/opt/input.csv'  # Remplacez par le chemin réel de votre fichier CSV

    # Lire le fichier CSV
    df = spark.read.csv(input_csv, header=True, inferSchema=True)

    # Sauvegarder le DataFrame dans un fichier Parquet
    parquet_path = "/tmp/read_df.parquet"
    df.write.mode("overwrite").parquet(parquet_path)

    spark.stop()

    # Passer le chemin du fichier Parquet via XCom
    kwargs['ti'].xcom_push(key='parquet_path', value=parquet_path)

# Fonction pour transformer les données en utilisant le fichier Parquet et renvoyer le fichier Parquet transformé
def transform_data(**kwargs):
    spark = SparkSession.builder \
        .appName("Airflow PySpark Data Transformation Example") \
        .getOrCreate()

    # Récupérer le chemin du fichier Parquet via XCom
    ti = kwargs['ti']
    parquet_path = ti.xcom_pull(key='parquet_path', task_ids='read_csv')

    # Charger le DataFrame à partir du fichier Parquet
    df = spark.read.parquet(parquet_path)

    # Exemple de transformation : filtrer les lignes où la colonne 'value' est supérieure à 1
    transformed_df = df.filter(col('age') > 25)

    # Sauvegarder le DataFrame transformé dans un fichier Parquet
    transformed_parquet_path = "/tmp/transformed_df.parquet"
    transformed_df.write.mode("overwrite").parquet(transformed_parquet_path)

    spark.stop()

    # Passer le chemin du fichier Parquet transformé via XCom
    kwargs['ti'].xcom_push(key='transformed_parquet_path', value=transformed_parquet_path)

# Fonction pour sauvegarder les résultats en CSV en utilisant le fichier Parquet transformé
def save_data(**kwargs):
    spark = SparkSession.builder \
        .appName("Airflow PySpark Data Save Example") \
        .getOrCreate()

    # Récupérer le chemin du fichier Parquet transformé via XCom
    ti = kwargs['ti']
    transformed_parquet_path = ti.xcom_pull(key='transformed_parquet_path', task_ids='transform_data')

    # Charger le DataFrame transformé depuis le fichier Parquet
    df = spark.read.parquet(transformed_parquet_path)

    # Sauvegarder les données transformées dans un fichier CSV de sortie final
    output_csv = '/tmp/output_file.csv'  # Remplacez par le chemin réel du fichier CSV final
    
    # Sauvegarder les données en format CSV
    df.write.mode("overwrite").option("header", "true").csv(output_csv)

    spark.stop()

# Définir le DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 9),  # Remplacez par votre date de début souhaitée
    'retries': 1,
}

with DAG('pyspark_csv_read_transform_save_csv_dag', default_args=default_args, schedule_interval=None) as dag:
    # Tâche pour lire le CSV
    read_csv_task = PythonOperator(
        task_id='read_csv',
        python_callable=read_csv,
        provide_context=True,  # Permet d'utiliser XCom
    )

    # Tâche pour transformer les données
    transform_data_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        provide_context=True,  # Permet d'utiliser XCom
    )

    # Tâche pour sauvegarder les données transformées en CSV
    save_data_task = PythonOperator(
        task_id='save_data',
        python_callable=save_data,
        provide_context=True,  # Permet d'utiliser XCom
    )

    # Définir les dépendances entre les tâches
    read_csv_task >> transform_data_task >> save_data_task

