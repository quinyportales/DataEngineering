"""This module implements a DAG to process the COVID data"""
from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from config_covid.config_covid import COVID_URL
from dags.base_dag import BaseDAG
from src.covid_data import CovidData


class CovidDAG(BaseDAG):
    """Class to to collect data from COVID API, 
    transform the data and store it into MinIo """
    def __init__(self) -> None:
        """Initializes the DAG and the superclass attributes"""
        dag_id  = 'covid_dag'
        schedule = '@daily'
        super().__init__(dag_id, schedule)

    def create_tasks(self) -> None:
        covid_instance = CovidData(COVID_URL)
        extract_task_arg = {
            'task_id' : 'extract_covid_data',
            'python_callable' : covid_instance.extract_data
            }
        self.logger.info('Creating task extract_covid_data')
        extract_covid_data = self.create_python_task(**extract_task_arg)


        transform_task_arg = {
            'task_id' : 'transform_covid_data',
            'python_callable' : covid_instance.transform_data
            }
        self.logger.info('Creating task transform_covid_data')
        transform_covid_data = self.create_python_task(**transform_task_arg)

        trigger_next_postgres_raw_dag_task_arg ={
            'task_id': 'trigger_postgres_raw_dag',
            'trigger_dag_id': 'postgres_raw_dag',
            'execution_date': '{{ execution_date }}',
            'reset_dag_run': True,
            'wait_for_completion': False,
            'trigger_rule': TriggerRule.ALL_SUCCESS
        }
        self.logger.info('Triggering the next DAG postgres_raw_dag')
        trigger_next_postgres_raw_dag_task =(
            self.trigger_dag(**trigger_next_postgres_raw_dag_task_arg))

        #task chaining
        extract_covid_data >> transform_covid_data >> trigger_next_postgres_raw_dag_task


dag = CovidDAG().build()
