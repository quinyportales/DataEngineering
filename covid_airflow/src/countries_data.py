"""This module contains the CountriesData class for countries data processing """
from pyspark.sql import DataFrame
import pyspark.sql.functions as f
from src.api_get import APIHandler
from config_covid.config_covid import (
    spark_session, get_minio_client,
    countries_raw_path,
    countries_transf_path)

class CountriesData(APIHandler):
    """Class to transform the data Countries data
    fetched from the API endpoint"""
    def __init__(self, API_URL : str) -> None:
        """Initializes the CountriesData object with the API URL."""
        self.countries_raw_df : DataFrame = None
        self.countries_transf_df : DataFrame = None
        super().__init__(API_URL)

    def extract_data(self) -> None:
        """Extracts data from the API, converts it to a Spark DataFrame, 
        and saves the raw data to MinIO."""
        spark = spark_session()
        with spark_session() as spark:
            self.logger.info('Starting extract_data from CountriesData')
            minio_client = get_minio_client()
            try:
                self.logger.info('Starting  extract_data from CountriesData')
                api_response = self.extract_data_api()

                self.countries_raw_df = self.transform_to_df(spark, api_response)

                self.logger.info("Saving raw data to MinIO")
                minio_client.upload_minio(self.countries_raw_df, countries_raw_path)

            except Exception as e:
                self.logger.error('Error running extract_data from CountriesData: %s', e)


    def transform_data(self) -> None:
        """Loads the raw data from MinIO, performs cleaning and transformation,
            and saves the transformed data back to MinIO."""
        with spark_session() as spark:
            self.logger.info('Starting transform_data from CountriesData')
            minio_client = get_minio_client()

            try:
                raw_df = minio_client.fetch_df_from_minio(spark, countries_raw_path)
                transf_df = self.clean_column_names(raw_df)
                #transforming the data and storing into minio
                self.countries_transf_df = self.countries_cast_cols(transf_df)
                #storing data into Minio
                self.logger.info("Saving transformed data to MinIO")
                minio_client.upload_minio(self.countries_transf_df, countries_transf_path)

            except Exception as e:
                self.logger.error('Error running transform_data from CountriesData: %s', e)

    def clean_column_names (self, raw_df : DataFrame) -> DataFrame:
        """Selects and renames relevant fields from the raw DataFrame,
        and adds a column for the ingestion date."""
        self.logger.info('Initiating clean_column_names')
        #field selenction and column rename
        raw_df = raw_df.select(
            f.col('id').alias('country_id'),
            f.col('name').alias('country_name'),
            f.col('region.value').alias('region'),
            f.col('incomeLevel.value').alias('income_level'))
        self.logger.info('Field selection completed.')

        #adding the ingestion date
        raw_df = raw_df.withColumn('ingested_date', f.current_date())
        return raw_df

    def countries_cast_cols(self, raw_df: DataFrame) -> DataFrame:
        """Casts DataFrame columns to appropriate types and creates an 
        'ingested_year_month' column."""
        self.logger.info('Starting covid_cast_cols from CountriesData')
        try:
            transf_df = (raw_df
                    .withColumn('country_id', f.col('country_id').cast('string'))
                    .withColumn('country_name',f.col('country_name').cast('string'))
                    .withColumn('region', f.col('region').cast('string'))
                    .withColumn('income_level',
                                f.col('income_level').cast('string'))
                    .withColumn('ingested_year_month',
                                f.date_format(f.col('ingested_date'), 'yyyy/MM'))
                )
            return transf_df
        except Exception as e:
            self.logger.error('Error casting columns in countries_cast_cols: %s', e)
            raise
