from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
default_args = {
'owner'                 : 'airflow',
'description'           : 'Use of the DockerOperator',
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
  k8s.V1EnvVar(name='MG_CATALOGUE_USERNAME_STAGING', value='admin'),
  k8s.V1EnvVar(name='MG_CATALOGUE_PASSWORD_STAGING', value=''),
  k8s.V1EnvVar(name='MG_CATALOGUE_URL_PROD', value='https://emx2.test.molgenis.org/'),
  k8s.V1EnvVar(name='MG_CATALOGUE_USERNAME_PROD', value='admin'),
  k8s.V1EnvVar(name='MG_CATALOGUE_PASSWORD_PROD', value='')
]

with DAG(dag_id='docker_dag', default_args=default_args, catchup=False) as dag:
    t1 = BashOperator(
      task_id='print_current_date',
      bash_command='date'
    )
    t2 = KubernetesPodOperator(namespace='default',
      task_id="transfrom-job",
      namespace='airflow',
      image="molgenis/molgenis-py-catalogue-transform:1.0.15",
      # cmds=["Python","-c"],
      # arguments=["print('hello world')"],
      # labels={"foo": "bar"},
      env=init_environments,
      name="transform-job",
      get_logs=True,
      dag=dag
    )
    t3 = BashOperator(
    task_id='print_hello',
    bash_command='echo "hello world"'
    )
t1 >> t2 >> t3