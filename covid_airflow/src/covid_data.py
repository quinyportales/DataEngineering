"""This module contains the Covid_Data class for covid data processing """
from pyspark.sql import DataFrame
import pyspark.sql.functions as f
from src.api_get import APIHandler
from config_covid.config_covid import (
    spark_session, get_minio_client,
    covid_raw_path,
    covid_transf_path)


class CovidData (APIHandler):
    """Class to transform the data Covid data
    fetched from the API endpoint"""
    def __init__(self, API_URL : str) -> None:
        self.covid_raw_df : DataFrame = None
        self.covid_transf_df : DataFrame = None
        super().__init__(API_URL)

    def extract_data(self) -> None:
        """Extracts data from the API, converts it to a Spark DataFrame, 
        and saves the raw data to MinIO."""
        spark = spark_session()
        with spark_session() as spark:
            minio_client = get_minio_client()
            self.logger.info('Starting extract_data from CovidData')

            try:
                api_response = self.extract_data_api()
                self.covid_raw_df = self.transform_to_df(spark, api_response)

                if self.covid_raw_df is None or self.covid_raw_df.rdd.isEmpty():
                    self.logger.warning("Extracted DataFrame is empty. Skipping upload.")
                    return

                self.logger.info("Raw dataframe preview:")
                self.covid_raw_df.show(5, truncate=False)

                self.logger.info("Saving raw data to MinIO")
                minio_client.upload_minio(self.covid_raw_df, covid_raw_path)
            except Exception as e:
                self.logger.error('Error running extract_data from CovidData: %s', e)

    def transform_data(self) -> None:
        """Loads the raw data from MinIO, performs cleaning and transformation,
            and saves the transformed data back to MinIO."""
        spark = spark_session()
        with spark_session() as spark:
            minio_client = get_minio_client()
            self.logger.info('Starting transform_data from CovidData')

            try:
                raw_df = minio_client.fetch_df_from_minio(spark, covid_raw_path)
                transf_df = self.clean_column_names(raw_df)

                #transforming the data and storing into minio
                self.covid_transf_df = self.covid_cast_cols(transf_df)

                #storing data into Minio
                self.logger.info("Saving transformed data to MinIO")
                minio_client.upload_minio(self.covid_transf_df, covid_transf_path)

            except Exception as e:
                self.logger.error('Error running transform_data from CovidData: %s', e)

    def clean_column_names (self, raw_df : DataFrame) -> DataFrame:
        """Selects and renames relevant fields from the raw DataFrame,
        and adds a column for the ingestion date."""
        self.logger.info('Initiating clean_column_names')
        #field selenction and column rename
        raw_df = raw_df.select(
            f.col('Country_text').alias('country_name'),
            f.col('Active Cases_text').alias('active_cases'),
            f.col('Last Update').alias('last_update'),
            f.col('New Cases_text').alias('new_cases'),
            f.col('New Deaths_text').alias('new_deaths'),
            f.col('Total Cases_text').alias('total_cases'),
            f.col('Total Deaths_text').alias('total_deaths'),
            f.col('Total Recovered_text').alias('total_recovered')
        )

        #adding the ingestion date
        raw_df = raw_df.withColumn('ingested_date', f.current_date())
        return raw_df

    def covid_cast_cols(self, raw_df: DataFrame) -> DataFrame:
        """Casts DataFrame columns to appropriate types and creates"""
        self.logger.info('Starting covid_cast_cols from CovidData')
        try:
            transf_df = (raw_df
                       .withColumn('active_cases',
                                   f.regexp_replace('active_cases', '[^0-9]', '').cast('integer'))
                       .withColumn('new_cases',
                                   f.regexp_replace('new_cases', '[^0-9]', '').cast('integer'))
                       .withColumn('new_deaths',
                                   f.regexp_replace('new_deaths', '[^0-9]', '').cast('integer'))
                       .withColumn('total_cases',
                                   f.regexp_replace('total_cases', '[^0-9]', '').cast('integer'))
                       .withColumn('total_deaths',
                                   f.regexp_replace('total_deaths', '[^0-9]', '').cast('integer'))
                       .withColumn('total_recovered',
                                   f.regexp_replace('total_recovered', '[^0-9.]', '').cast('float'))
                       .withColumn('last_update',
                                   f.to_date('last_update', 'yyyy-MM-dd HH:mm'))
            )

            self.logger.info('Transformation completed')
            return transf_df

        except Exception as e:
            self.logger.error("Error applying the transformations: %s", e)
            raise
