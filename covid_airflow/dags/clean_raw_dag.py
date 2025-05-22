"""This module implements the class Clean_DAG 
to clear the data from raw tables schema"""
from airflow import DAG
from dags.base_dag import BaseDAG

class CleanDAG(BaseDAG):
    """Clean the raw schema from postgress"""
    def __init__(self):
        """Initializes the DAG and the superclass attributes"""
        dag_id  = 'clean_raw_dag'
        schedule = None
        super().__init__(dag_id, schedule)

    def create_tasks(self):
        """Defines DAG tasks and their dependencies."""

        clean_raw_schema_task_arg = {
            'task_id' : 'clean_raw_schema_task',
            'sql': 'sql_clean.sql',
            'postgres_conn_id' : self.get_connection()
            }
        self.logger.info('Creating  clean_raw_schema_task')
        clean_raw_schema_task = self.create_postgres_task(**clean_raw_schema_task_arg)

        clean_raw_schema_task


dag = CleanDAG().build()
