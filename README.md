# AirFlow DAGS
This repository contains the DAG configuration for the Airflow pipeline. 

## Dags
We develop a dag for each transformation pipeline in our infrastructure.

We use Airflow and Kubernetes to deploy jobs. For parameters we define environment variables and we are gogin to use the hashicorp vault. You can override them in a manual start of the job. The secrets that are used from the vault are set per job. The paths to the hashicorp vault are predefined.

### Catalogue
You can override the values by submitting this block of `json`.

```json
{
    "dag_run.conf.networks": "LifeCycle, ATHLETE, LongITools",
    "dag_run.conf.cohorts": "NFBC1966, NFBC1986, KANC",
    "dag_run.conf.staging_url": "https://data-catalogue-staging.molgeniscloud.org/",
    "dag_run.conf.staging_username": "admin",
    "dag_run.conf.staging_password": "xxxx",
    "dag_run.conf.prod_url": "https://data-catalogue.molgeniscloud.org/",
    "dag_run.conf.catalogue_username": "admin",
    "dag_run.conf.catalogue_password": "xxxx"
}
```

You can leave out the parameters you do not want to override.