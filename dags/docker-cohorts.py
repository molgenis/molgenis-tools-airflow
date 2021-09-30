from kubernetes.client import models as k8s
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
default_args = {
  'owner'                 : 'airflow',
  'description'           : 'Catalogue cohort etl job',
  'depend_on_past'        : False,
  'start_date'            : datetime(2018, 1, 3),
  'email_on_failure'      : False,
  'email_on_retry'        : False,
  'retries'               : 1,
  'retry_delay'           : timedelta(minutes=5)
}

with DAG(dag_id='cohorts-etl_dag', default_args=default_args, catchup=False) as dag:
    task = KubernetesPodOperator(
      task_id="cohorts-etl-job",
      namespace='airflow',
      image="molgenis/molgenis-py-cohorts-etl:latest",
      env_vars={'MG_CATALOGUE_URL': '{{ var.value.catalogue_url }}', 'MG_ETL_USERNAME': '{{ var.value.etl_username }}', 'MG_ETL_PASSWORD': '{{ var.value.etl_password }}', 'MG_SYNC_SOURCES': '{{ var.value.sync_sources }}', 'MG_SYNC_TARGET': '{{ var.value.sync_target }}'},  
      name="cohort-etl-job",
      get_logs=True,
      dag=dag
    )
task