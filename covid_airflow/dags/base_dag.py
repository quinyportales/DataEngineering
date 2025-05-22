"""This module implements the class BaseDAG which 
is the base class to define all DAGs for Airflow."""

import logging
from datetime import datetime
from abc import ABC, abstractmethod
from airflow import DAG
from airflow.models import DagModel
from airflow.models import Connection
from airflow import settings
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.session import provide_session
from airflow.utils.trigger_rule import TriggerRule

class BaseDAG(ABC):
    """ Abstract base class for defining Airflow DAGs."""
    def __init__(self, dag_id: str, schedule: str,
                 start_date : datetime =  datetime(2025, 5, 1)) -> None:
        """Initializes the DAG attributes"""
        self.dag_id = dag_id
        self.start_date =  start_date
        self.schedule = schedule
        self.dag = None

        logging.basicConfig(filename='logs/CovidAirflowApp.log', level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)


    def create_python_task(self, task_id, python_callable, op_kwargs=None) -> PythonOperator:
        """Creates a PythonOperator task."""
        return PythonOperator(
            task_id=task_id,
            python_callable=python_callable,
            op_kwargs=op_kwargs or {},
            dag=self.dag
        )

    def create_postgres_task(self, task_id: str,
                             sql: str,
                             postgres_conn_id: str = "postgres_default") -> PostgresOperator:
        """ Creates a PostgresOperator task."""
        return PostgresOperator(
            task_id=task_id,
            sql=sql,
            postgres_conn_id=postgres_conn_id,
            dag=self.dag
        )

    def trigger_dag(
        self,
        task_id: str,
        trigger_dag_id: str,
        execution_date: str = '{{ execution_date }}',
        wait_for_completion: bool = False,
        reset_dag_run: bool = True,
        trigger_rule: str = TriggerRule.ALL_SUCCESS,
        **kwargs
    ) -> TriggerDagRunOperator:
        """Triggers another DAG using TriggerDagRunOperator."""
        return TriggerDagRunOperator(
            task_id=task_id,
            trigger_dag_id=trigger_dag_id,
            execution_date=execution_date,
            wait_for_completion=wait_for_completion,
            reset_dag_run=reset_dag_run,
            trigger_rule=trigger_rule,
            dag=self.dag,
            **kwargs
        )

    def build(self, catchup=False) -> DAG:
        """Builds the Airflow DAG with tasks."""
        with DAG(
            dag_id=self.dag_id,
            start_date=self.start_date,
            schedule_interval=self.schedule,
            catchup=catchup,
            max_active_runs=1,
            concurrency=1,
            template_searchpath=['/opt/airflow/include'] 
        ) as dag:
            self.dag = dag
            self.create_tasks()

        session = settings.Session()
        dag_model = session.query(DagModel).filter(DagModel.dag_id == self.dag_id).first()
        if dag_model:
            dag_model.is_paused = False
            session.commit()
        session.close()
        return dag

    @provide_session
    def activate_dag(self, session=None):
        """Despausa el DAG si está pausado."""
        dag_model = session.query(DagModel).filter_by(dag_id=self.dag_id).first()
        if dag_model and dag_model.is_paused:
            dag_model.is_paused = False
            session.commit()

    def get_connection(self) -> str:
        """Create Airflow connection if not exists, then return conn_id."""
        conn_id = 'postgres_warehouse'
        conn = Connection(
            conn_id=conn_id,
            conn_type='postgres',
            host='warehouse_postgres',
            schema='data_warehouse',
            login='airflow',
            password='airflow',
            port=5432
        )

        session = settings.Session()
        if not session.query(Connection).filter_by(conn_id=conn_id).first():
            session.add(conn)
            session.commit()

        return conn_id

    @abstractmethod
    def create_tasks(self) -> None :
        """Abstract method to create tasks in the DAG.
        Must be implemented by subclasses"""
        pass
