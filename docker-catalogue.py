from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator
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
with DAG(dag_id='docker_dag', default_args=default_args, catchup=False) as dag:
    t1 = BashOperator(
    task_id='print_current_date',
    bash_command='date'
    )
    t2 = DockerOperator(
    task_id='docker_command',
    image='molgenis/molgenis-py-catalogue-transform:1.0.15',
    api_version='auto',
    auto_remove=True,
    # command="./run.py",
    # docker_url="tcp://docker-proxy:2375",
    # network_mode="bridge",
    tty=True,
    # xcom_all=True,
    environment={ 'MG_CATALOGUE_NETWORKS':'LifeCycle, ATHLETE, LongITools',
      'MG_CATALOGUE_COHORTS':'NFBC1966, NFBC1986, KANC',
      'MG_CATALOGUE_URL_STAGING':'https://data-catalogue-staging.molgeniscloud.org/',
      'MG_CATALOGUE_USERNAME_STAGING':'admin',
      'MG_CATALOGUE_PASSWORD_STAGING':'',
      'MG_CATALOGUE_URL_PROD':'https://emx2.test.molgenis.org/',
      'MG_CATALOGUE_USERNAME_PROD':'admin',
      'MG_CATALOGUE_PASSWORD_PROD':''}
    )
    t3 = BashOperator(
    task_id='print_hello',
    bash_command='echo "hello world"'
    )
t1 >> t2 >> t3