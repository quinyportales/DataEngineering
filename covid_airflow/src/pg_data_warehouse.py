"""This module implements the class PG_DataWarehoue which fetch the data
from postgres raw schema  processed and loads it into DW schema"""
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as f
from pyspark.sql.window import Window
from src.pg_raw import PostgresRaw
from config_covid.config_covid import spark_session

class PGWarehouse (PostgresRaw):
    """Class to extract data from postgres raw schema and load it 
    into separate Postgres schema to serve as a datawarehouse """

    def __init__(self) -> None:
        """ Initializes the PGWarehouse instance and call the superclass initializer."""
        self.raw_covid : DataFrame = None
        self.raw_countries : DataFrame = None
        super().__init__()

    def create_schema(self, schema_name='dw_data_schema') -> None:
        """Create the data warehouse schema in Postgres if it does not exist."""
        super().create_schema(schema_name=schema_name)

    def load_data_pg (self) -> None:
        """ Extracts data from raw Postgres schema, clean it, and load into DW schema tables"""
        with spark_session() as spark:
            self.raw_covid = self.fetch_from_postgres(spark, self.jdbc_options, 'covid_table')
            self.raw_countries = self.fetch_from_postgres(
                 spark, self.jdbc_options, 'countries_table')
            self.transf_data_covid = self.clean_covid(self.raw_covid)
            self.transf_data_countries = self.clean_countries(self.raw_countries)

            try:
                self.logger.info('Loading covid dataframe into postgress schema')
                self.write_df_into_pg(self.transf_data_covid,
                                      'covid_table', schema= 'dw_data_schema')

                self.logger.info('Loading dataframecountries into postgress schema')
                self.write_df_into_pg(self.transf_data_countries,
                                      'countries_table', schema= 'dw_data_schema')
            except Exception as e:
                self.logger.error('Error running looading_data_ps: %s', e)

    def fetch_from_postgres(self, spark: SparkSession ,
                            jdbc_options, table : str,
                            schema ='raw_data_schema') -> DataFrame:
        """Fetch a table from Postgres as a Spark DataFrame."""
        full_table = f"{schema}.{table}"
        self.logger.info('Initiating read_data_postgres ')
        try:
            df =( spark.read
                    .format('jdbc')
                    .option('url', self.jdbc_url )
                    .option('dbtable', full_table)
                    .option('user', jdbc_options['user'])
                    .option('password', jdbc_options['password'])
                    .option('driver', "org.postgresql.Driver")
                    .load())
            self.logger.info('Dataframe loadded from Postgres schema %s:', schema)
            df.show(5, truncate=False)
            return df
        except Exception as e:
            self.logger.error('Error running fetch_from_postgress: %s', e)
            return None

    def clean_covid(self, df_covid: DataFrame) -> DataFrame:
        """Clean COVID data by removing duplicates and null values."""
        self.logger.info('Removing duplicated values from covid data')
        windows_spec = Window.partitionBy('country_name').orderBy(f.col('last_update').desc())

        df_covid = (df_covid
                    .withColumn('row_num', f.row_number().over(windows_spec))
                    .filter(f.col('row_num') == 1)
                    .drop('row_num'))
        df_covid = df_covid.dropDuplicates()
        self.logger.info('Removing nulls values from covid data')
        df_covid = df_covid.na.drop()
        return df_covid

    def clean_countries(self, df_countries: DataFrame) -> DataFrame:
        """ Clean countries data by removing duplicates and null values."""
        self.logger.info('Removing duplicated values from countries data')

        window_spec = Window.partitionBy('country_id').orderBy(f.col('ingested_date').desc())
        df_countries = (df_countries
                        .withColumn('row_num', f.row_number().over(window_spec))
                        .filter(f.col('row_num') == 1)
                        .drop('row_num'))
        df_countries = df_countries.dropDuplicates()
        self.logger.info('Removing null values from countries data')
        df_countries = df_countries.na.drop()
        return df_countries
