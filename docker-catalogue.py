from kubernetes.client import models as k8s
from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
default_args = {
  'owner'                 : 'airflow',
  'description'           : 'Catalogue transform job',
  'depend_on_past'        : False,
  'start_date'            : datetime(2018, 1, 3),
  'email_on_failure'      : False,
  'email_on_retry'        : False,
  'retries'               : 1,
  'retry_delay'           : timedelta(minutes=5)
}

init_environments = [
  k8s.V1EnvVar(name='MG_CATALOGUE_NETWORKS', value='LifeCycle, ATHLETE, LongITools'), 
  k8s.V1EnvVar(name='MG_CATALOGUE_COHORTS', value='NFBC1966, NFBC1986, KANC'),
  k8s.V1EnvVar(name='MG_CATALOGUE_URL_STAGING', value='https://data-catalogue-staging.molgeniscloud.org/'),
  k8s.V1EnvVar(name='MG_CATALOGUE_USERNAME_STAGING', value="{{ dag_run.conf.staging_username | default('admin', true) }}"),
  k8s.V1EnvVar(name='MG_CATALOGUE_PASSWORD_STAGING', value="{{ dag_run.conf.staging_password | default('xxxxx', true) }}"),
  k8s.V1EnvVar(name='MG_CATALOGUE_URL_PROD', value='https://emx2.test.molgenis.org/'),
  k8s.V1EnvVar(name='MG_CATALOGUE_USERNAME_PROD', value="{{ dag_run.conf.catalogue_username | default('admin', true) }}"),
  k8s.V1EnvVar(name='MG_CATALOGUE_PASSWORD_PROD', value="{{ dag_run.conf.catalogue_password | default('xxxxx', true) }}")
]

with DAG(dag_id='catalogue-transform_dag', default_args=default_args, catchup=False) as dag:
    task = KubernetesPodOperator(
      task_id="transfrom-job",
      namespace='airflow',
      image="molgenis/molgenis-py-catalogue-transform:latest",
      env_vars=init_environments,
      name="transform-job",
      get_logs=True,
      dag=dag
    )
task