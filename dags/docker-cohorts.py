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

init_environments = [
  k8s.V1EnvVar(name='MG_CATALOGUE_URL', value="{{ dag_run.conf.catalogue_url | default('https://emx2.dev.molgenis.org/', true) }}"),
  k8s.V1EnvVar(name='MG_ETL_USERNAME', value="{{ dag_run.conf.etl_username | default('admin', true) }}"),
  k8s.V1EnvVar(name='MG_ETL_PASSWORD', value="{{ dag_run.conf.etl_password | default('xxxx', true) }}"),
  k8s.V1EnvVar(name='MG_SYNC_SOURCES', value="{{ dag_run.conf.sync_sources | default('', true) }}"),
  k8s.V1EnvVar(name='MG_SYNC_TARGET', value="{{ dag_run.conf.sync_target | default('', true) }}"),
 ]

with DAG(dag_id='cohorts-etl_dag', default_args=default_args, catchup=False) as dag:
    task = KubernetesPodOperator(
      task_id="cohorts-etl-job",
      namespace='airflow',
      image="molgenis/molgenis-py-cohorts-etl:latest",
      env_vars=init_environments,
      name="cohort-etl-job",
      get_logs=True,
      dag=dag
    )
task