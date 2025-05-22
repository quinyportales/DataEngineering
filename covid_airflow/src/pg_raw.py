"""This module implements the class PostgresRaw which fetches data
from Minio and loads it into a schema in Postgres"""
import logging
from typing import Generator
from contextlib import contextmanager
import psycopg2
from pyspark.sql import DataFrame
from config_covid.config_covid import (
    get_jdbc_url, get_jdbc_options,
    get_minio_client, spark_session,
    covid_transf_path,
    countries_transf_path)

class PostgresRaw:
    """Class to extract data from MinIO storage and load it 
    into separate Postgres schema for raw tables """

    def __init__(self) -> None:
        """ Initialize PostgresRaw with JDBC connection
        details and logger """
        self.transf_data_covid: DataFrame = None
        self.transf_data_countries: DataFrame = None
        self.jdbc_url : str = get_jdbc_url()
        self.jdbc_options : dict = get_jdbc_options()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    @contextmanager
    def postgres_connection(self, jdbc_options : dict) -> Generator:
        """Context manager to handle PostgreSQL connection and cursor"""
        connection = psycopg2.connect(**jdbc_options)
        connection.autocommit = True
        cursor = connection.cursor()

        try:
            yield connection, cursor
            connection.commit()
        except Exception as e:
            self.logger.error("Error during DB operation: %s", e)
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    def create_schema(self, schema_name='raw_data_schema') -> None :
        """Creates a schema in Postgres if it does not already exist """
        with self.postgres_connection(self.jdbc_options) as (connection, cursor):
            self.logger.info('Starting create_schema from PostgreRaw')
            cursor.execute(
                "SELECT schema_name FROM information_schema.schemata "
                "WHERE schema_name = %s",
                (schema_name,)
            )
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(f'CREATE SCHEMA "{schema_name}"')
                self.logger.info("Schema %s created.", schema_name)
            else:
                self.logger.info("Schema %s already exists.", schema_name)

    def load_data_pg(self) -> None :
        """Loads transformed data from MinIO into Postgres tables"""
        with spark_session() as spark:
            minio_client = get_minio_client()
            self.logger.info('Starting load_data from CPostgresRaw')
            try:
                self.transf_data_covid = (minio_client
                                          .fetch_df_from_minio(spark, covid_transf_path))
                self.transf_data_countries = (minio_client
                                              .fetch_df_from_minio(spark, countries_transf_path))
                self.logger.info('Loading dataframe covid_df into postgress schema')
                self.write_df_into_pg(self.transf_data_covid, 'covid_table')
                self.logger.info('Loading dataframe countries_df into postgress schema')
                self.write_df_into_pg(self.transf_data_countries, 'countries_table')
            except Exception as e:
                self.logger.error('Error running looading_data_ps: %s', e)

    def write_df_into_pg(self, df: DataFrame,
                         table: str,
                         schema: str = 'raw_data_schema') -> None :
        """Writes a Spark DataFrame into a Postgres table using JDBC."""
        full_table = f"{schema}.{table}"
        self.logger.info("Writing to %s", full_table)
        (df.write
            .format("jdbc")
            .option("url", self.jdbc_url)
            .option("dbtable", full_table)
            .option("user", self.jdbc_options["user"])
            .option("password", self.jdbc_options["password"])
            .option("driver", "org.postgresql.Driver")
            .mode("overwrite")
            .save())
