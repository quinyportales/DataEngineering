"""This module implements the class Analysis_DAG 
to join the data tables"""
from airflow import DAG
from dags.base_dag import BaseDAG
from src.analysis_data import AnalysisCovid

class AnalysisDAG(BaseDAG):
    """Class to select data from joined tables (covid and financial countries data) 
    from data warehouse tables schema to see the dependency. """
    def __init__(self) -> None:
        dag_id = 'analysis_dag'
        schedule = None
        super().__init__(dag_id, schedule)

    def create_tasks(self) -> None:
        """Defines DAG tasks and their dependencies."""
        analysis_instance = AnalysisCovid()

        join_data_task_arg={
            'task_id' : 'join_data_task',
            'sql': 'sql_analysis.sql',
            'postgres_conn_id' : self.get_connection()
        }
        self.logger.info('Creating task join_data_task')
        join_data_task = self.create_postgres_task(**join_data_task_arg)

        load_join_data_task_arg={
            'task_id' : 'load_join_data_task',
            'python_callable' : analysis_instance.load_joined_table
        }
        self.logger.info('Creating load_join_data_task')
        load_join_data_task = self.create_python_task(**load_join_data_task_arg)

        join_data_task >> load_join_data_task

dag= AnalysisDAG().build()
