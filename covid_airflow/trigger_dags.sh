#!/bin/bash

EXECUTION_DATE=$(date +"%Y-%m-%d")

CONTAINER_NAME="covid_airflow-airflow-webserver-1"

echo " Triggering DAG: countries_dag  $EXECUTION_DATE ..."
docker exec -it $CONTAINER_NAME airflow dags trigger -e $EXECUTION_DATE countries_dag
docker exec -it $CONTAINER_NAME airflow dags trigger -e $EXECUTION_DATE covid_dag
docker exec -it $CONTAINER_NAME airflow dags trigger -e $EXECUTION_DATE postgres_raw_dag
docker exec -it $CONTAINER_NAME airflow dags trigger -e $EXECUTION_DATE datawarehouse_dag
docker exec -it $CONTAINER_NAME airflow dags trigger -e $EXECUTION_DATE clean_raw_dag
docker exec -it $CONTAINER_NAME airflow dags trigger -e $EXECUTION_DATE analysis_dag

echo "DAGs has been completed"

