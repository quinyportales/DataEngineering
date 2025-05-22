"""This module implements a DAG to process the postgres raw schema"""
from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from dags.base_dag import BaseDAG
from src.pg_data_warehouse import PGWarehouse


class DatawarehouseDAG(BaseDAG):
    """Extract data from postgres and loads it 
    into separate Postgres schema to serves as a warehouse"""
    def __init__(self):
        """Initializes the DAG and the superclass attributes"""
        dag_id  = 'datawarehouse_dag'
        schedule = None
        super().__init__(dag_id, schedule)

    def create_tasks(self):
        """Defines DAG tasks and their dependencies."""
        data_warehouse_instance = PGWarehouse()

        create_dw_schema_task_arg = {
            'task_id' : 'create_dw_schema',
            'python_callable': data_warehouse_instance.create_schema
            }
        self.logger.info('Creating task create_dw_schema')
        create_DW_schema_task = self.create_python_task(**create_dw_schema_task_arg)

        load_data_pg_task_arg = {
            'task_id' : 'load_data_pg_task',
            'python_callable': data_warehouse_instance.load_data_pg
            }
        self.logger.info('Creating task load_data_pg_task')
        load_data_pg_task = self.create_python_task(**load_data_pg_task_arg)

        trigger_next_clean_dag_task_arg ={
            'task_id' : 'trigger_clean_raw_dag',
            'trigger_dag_id' : 'clean_raw_dag',
            'execution_date': '{{ execution_date }}',
            'reset_dag_run': True,
            'wait_for_completion': False,
            'trigger_rule': TriggerRule.ALL_SUCCESS
        }
        self.logger.info('Triggering the next DAG clean_raw_dag')
        trigger_next_clean_dag_task = self.trigger_dag(**trigger_next_clean_dag_task_arg)

        trigger_next_analysis_dag_task_arg ={
            'task_id' : 'trigger_analysis_dag',
            'trigger_dag_id' : 'analysis_dag',
            'execution_date': '{{ execution_date }}',
            'reset_dag_run': True,
            'wait_for_completion': False,
            'trigger_rule': TriggerRule.ALL_SUCCESS
        }
        self.logger.info('Triggering the next DAG analysis_dag')
        trigger_next_analysis_dag_task = self.trigger_dag(**trigger_next_analysis_dag_task_arg)


        create_DW_schema_task >> load_data_pg_task>>[trigger_next_clean_dag_task,
                                                     trigger_next_analysis_dag_task]

dag = DatawarehouseDAG().build()
