#!/bin/bash
# entrypoint.sh
export PYTHONPATH="${PYTHONPATH}:/opt/airflow"

#Initializing DB for the first time 
airflow db init

#Creating airflow user
airflow users create \
  --username airflow \
  --password airflow \
  --firstname Airflow \
  --lastname Admin \
  --role Admin \
  --email admin@example.com || true

exec airflow  "$@"
