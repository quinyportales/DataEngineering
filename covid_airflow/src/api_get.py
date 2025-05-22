"""Module to handle the API data collection"""
import logging
from typing import Any
from pyspark.sql import SparkSession, DataFrame
import requests
from requests.exceptions import RequestException

class APIHandler:
    """Class to fetch the Countries and Covid data from an API endpoint"""
    def __init__(self, api_url) -> None:
        """ Initialize the APIHandler instance with the API URL and configure logging."""
        self.url : str = api_url
        self.data : Any = None

        logging.basicConfig(filename='logs/CovidAirflowApp.log', level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def extract_data_api (self) -> Any:
        """Fetch data from the configured API URL"""
        self.logger.info("Starting extract_data_api from API %s", self.url)
        try:
            response = requests.get (self.url, timeout=60)
            if response.status_code == 200:
                self.data = response.json()
                if "worldbank.org" in self.url:
                    self.data = self.data[1]

                self.logger.info("Extracted %d records",
                                 len(self.data))
                self.logger.info(
                    "Raw_data content: %s  Type of: %s",
                    self.data[:5],
                    type(self.data))

            return self.data
        except RequestException as e:
            self.logger.error("API request failed: %s", e)
            raise

    def transform_to_df(self, spark: SparkSession, data: Any) -> DataFrame :
        """ Convert the raw API data into a Spark DataFrame"""
        return spark.createDataFrame(data)
