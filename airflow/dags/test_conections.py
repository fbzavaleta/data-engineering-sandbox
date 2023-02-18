# Core
from fileinput import filename
from unicodedata import name
from airflow import DAG
from airflow.hooks.mysql_hook import MySqlHook
from airflow.hooks.S3_hook import S3Hook

#APIs
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

#Libs
from datetime import datetime

#constants
dags_root_folder = "/opt/airflow/dags"

default_args = {
    "0wner": "airflow",
    "start_date": datetime(2023, 2, 12),
    "catchup": False,
}

def get_files():
    import pandas as pd

    df_stagging = pd.read_csv(f"{dags_root_folder}/dumdata/movies.csv")
    print(df_stagging.head())

def test_database():
    import pandas as pd
    conn = MySqlHook(mysql_conn_id='mysql-local')
    query = "show databases;"
    results = conn.get_records(query)

    df_stagging = pd.read_csv(f"{dags_root_folder}/dumdata/movies.csv")

    for index, row in df_stagging.iterrows():
        query = f"""
            INSERT INTO movies ({','.join(df_stagging.columns)})
            VALUES ({','.join(['%s'] * len(df_stagging.columns))})
        """
        conn.run(query, autocommit=True, parameters=tuple(row))    

    print(results)
    
def test_s3():
    pass


with DAG(
    "teste-conections",
    default_args=default_args,
    description="Pipeline for testing the conextions",
    schedule_interval="@once",
) as dag:
    start_task = DummyOperator(task_id="start_task")
    
    extract_files = PythonOperator(
        task_id = "import_files",
        python_callable = get_files
    )

    start_task >> extract_files

    test_bash = BashOperator(
        task_id="test-bash",
        bash_command="ls /opt/airflow/dags",
    )

    extract_files >> test_bash

    test_database = PythonOperator(
        task_id = "test-database",
        python_callable = test_database
    )

    test_bash >> test_database

    test_s3 = PythonOperator(
        task_id = "test-s3",
        python_callable = test_s3
    )

    test_database >> test_s3    

    end_task = DummyOperator(task_id="end_task")

    test_s3 >> end_task