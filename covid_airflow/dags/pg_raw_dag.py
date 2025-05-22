"""This module implements a DAG to process the postgres raw schema"""
from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from dags.base_dag import BaseDAG
from src.pg_raw import PostgresRaw

class PgRawDAG(BaseDAG):
    """Extract data from MinIO and loads it 
    into separate Postgres schema for raw data"""
    def __init__(self):
        """Initializes the DAG and the superclass attributes"""
        dag_id  = 'postgres_raw_dag'
        schedule = None
        super().__init__(dag_id, schedule)

    def create_tasks(self):
        """Defines DAG tasks and their dependencies."""

        pg_raw_instance = PostgresRaw()

        create_raw_schema_task_arg = {
            'task_id' : 'create_raw_schema',
            'python_callable': pg_raw_instance.create_schema
            }
        self.logger.info('Creating task create_raw_schema')
        create_raw_schema_task = self.create_python_task(**create_raw_schema_task_arg)

        load_data_task_arg = {
            'task_id' : 'load_data_task',
            'python_callable': pg_raw_instance.load_data_pg
            }
        self.logger.info('Creating task load_data_task')
        load_data_task = self.create_python_task(**load_data_task_arg)

        trigger_next_dag_task_arg ={
            'task_id' : 'trigger_datawarehouse_dag',
            'trigger_dag_id' : 'datawarehouse_dag',
            'reset_dag_run': True,
            'wait_for_completion': False,
            'trigger_rule': TriggerRule.ALL_SUCCESS
        }
        self.logger.info('Triggering the next DAG datawarehouse_dag')
        trigger_next_dag_task = self.trigger_dag(**trigger_next_dag_task_arg)
        create_raw_schema_task >> load_data_task >> trigger_next_dag_task

dag = PgRawDAG().build()
