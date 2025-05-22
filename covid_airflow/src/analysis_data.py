"""This module implements the class AnalysisCovid which fetch the data
from postgres DW schema  and show the dependency between financial 
countries and covid data"""
import pyspark.sql.functions as f
from pyspark.sql import DataFrame
from src.pg_data_warehouse import PGWarehouse
from config_covid.config_covid import spark_session

class AnalysisCovid(PGWarehouse):
    """Class to join the covid and countries data loaded 
     from the datawarehouse """
    def __init__(self) -> None:
        """ Initializes the AnalysisCovid instance and call the superclass initializer."""
        self.joined_table: DataFrame = None
        super().__init__()

    def load_joined_table(self) -> None:
        """Joins the data from Covid and Countries table"""
        with spark_session() as spark:
            self.joined_table = self.fetch_from_postgres(
                spark, self.jdbc_options, 'joined_table', schema='dw_data_schema'
            )
            self.joined_table = (
                self.joined_table.groupBy('income_level')
                .agg(
                    f.sum('active_cases').alias('total_active_cases'),
                    f.avg('new_cases').alias('avg_new_cases'),
                    f.sum('total_deaths').alias('sum_total_deaths'),
                    f.avg('new_deaths').alias('avg_new_deaths'),
                    f.sum('total_recovered').alias('sum_total_recovered')
                )
            )
            self.joined_table.cache()
            self.joined_table.count()
            self.joined_table.show()
