"""This module implements the class MinIOHandler to handle the MinIo connection"""
import logging
from pathlib import Path
from minio import Minio
from minio.error import S3Error
from pyspark.sql import SparkSession,DataFrame

class MinionHandler:
    """A handler class for interacting with a MinIO server, including 
    bucket creation, uploading Spark DataFrames, and reading them back."""
    def __init__(self, minio_enpoint : str,
                 minio_access_key : str, minio_password : str,
                 bucket_name : str) -> None:
        """Initializes the MinionHandler instance and creates the bucket 
        if it does not already exist."""
        self.minio_end_point: str = minio_enpoint
        self.minio_client : Minio = Minio(
                            self.minio_end_point,
                            access_key= minio_access_key,
                            secret_key= minio_password,
                            secure=False
                            )
        self.bucket_name : str = bucket_name

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        if not self.minio_client.bucket_exists(bucket_name):
            try:
                self.minio_client.make_bucket(bucket_name)
                self.bucket_name = bucket_name
                self.logger.info('New Bucket Created %s ', self.bucket_name)
            except S3Error as e:
                if e.code != "BucketAlreadyOwnedByYou":
                    raise e
        self.logger.info('Bucket %s already exists — skipping creation', self.bucket_name)

    def upload_minio(self, df : DataFrame, path : Path) -> None:
        """Uploads a Spark DataFrame to MinIO as a Parquet file """
        self.logger.info('Initiating the MinIO dataframe uploading')
        minio_path = f"s3a://{self.bucket_name}/{path.as_posix()}"
        try:
            df.write.mode('overwrite').parquet(minio_path)

        except S3Error as err:
            self.logger.error('Error %s loading to MinIO', err)
            raise

    def fetch_df_from_minio(self, spark : SparkSession, path : Path) -> DataFrame:
        """Loads a Spark DataFrame from a Parquet file stored in MinIO."""
        minio_path = f"s3a://{self.bucket_name}/{path.as_posix()}"
        self.logger.info('Fetching raw data from MinIO: %s', minio_path)
        try:
            df = spark.read.parquet(minio_path)
            self.logger.info('DataFrame sucessfully created fetched from MinIO')
            return df
        except Exception as e:
            self.logger.error("Error when running fetch_df_from_minio: %s", e)
            raise
