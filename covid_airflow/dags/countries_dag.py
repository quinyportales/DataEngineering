"""This module implements a DAG to process the Countries data"""
from airflow import DAG
from config_covid.config_covid import  get_total_countries_url
from dags.base_dag import BaseDAG
from src.countries_data import CountriesData

class CountriesDAG(BaseDAG):
    """Class to to collect data from Countries information API, 
    transform data and store it into MinIo """
    def __init__(self) -> None:
        dag_id  = 'countries_dag'
        schedule = '@monthly'
        super().__init__(dag_id, schedule)

    def create_tasks(self) -> None:
        """Defines DAG tasks and their dependencies."""
        countries_url = get_total_countries_url()
        countries_instance = CountriesData(countries_url)
        extract_task_arg = {
            'task_id' : 'extract_countriesdata',
            'python_callable' : countries_instance.extract_data
            }
        self.logger.info('Creating task extract_countriesdata')
        extract_covid_data = self.create_python_task(**extract_task_arg)

        transform_task_arg = {
            'task_id' : 'transform_countries_data',
            'python_callable' : countries_instance.transform_data
            }
        self.logger.info('Creating task transform_countries_data')
        transform_countries_data = self.create_python_task(**transform_task_arg)
        extract_covid_data >> transform_countries_data

dag = CountriesDAG().build(catchup=True)
