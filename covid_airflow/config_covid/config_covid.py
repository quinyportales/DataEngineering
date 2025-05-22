"""Module to store all the the basic configuration for covid_airflow package"""
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Generator
from contextlib import contextmanager
from requests import get
from pyspark.sql import SparkSession
from src.minio_handler import MinionHandler

COVID_URL = 'https://covid-19.dataflowkit.com/v1'
BASE_COUNTRIES_URL = ' https://api.worldbank.org/v2/country'
APP_NAME = 'CovidAirflowApp'

MINIO_ACESS_KEY = 'minio'
MINIO_PASSWORD = 'minio123'
MINIO_ENDPOINT = 'minio:9000'
BUCKET_NAME = 'covid-bucket'
PATH_SQL = Path(__name__).parent / 'sql' / 'create_table.sql'

covid_raw_path = Path('raw') / 'covid_data'
covid_transf_path = Path('transf') / 'covid_data'

countries_raw_path = Path('raw') / 'countries_data'
countries_transf_path = Path('transf') / 'countries_data'


def get_spark_session() -> SparkSession:
    """Creates and returns a SparkSession configured with MinIO S3A support and necessary jars."""
    return (
        SparkSession.builder
        .appName(APP_NAME)
        .config("spark.jars",
                "/opt/airflow/jars/hadoop-aws-3.3.1.jar,"
                "/opt/airflow/jars/aws-java-sdk-bundle-1.11.901.jar,"
                "/opt/airflow/jars/postgresql-42.7.3.jar")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000")
        .config("spark.hadoop.fs.s3a.access.key", MINIO_ACESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", MINIO_PASSWORD)
        .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")
        .config("spark.speculation", "false")
        .config("spark.hadoop.fs.s3a.committer.name", "directory")
        .config("spark.hadoop.fs.s3a.committer.magic.enabled", "false")
        .config("spark.hadoop.fs.s3a.committer.staging.conflict-mode", "replace")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .getOrCreate()
    )

@contextmanager
def spark_session() -> Generator:
    """Context manager to provide a SparkSession and ensure it stops after use."""
    spark = get_spark_session()
    try:
        yield spark
    finally:
        spark.stop()

def get_minio_client() -> MinionHandler:
    """Instantiates and return a MinionHandler client configured for MinIO."""
    return MinionHandler(MINIO_ENDPOINT, MINIO_ACESS_KEY, MINIO_PASSWORD, BUCKET_NAME)

def get_total_countries_url () -> str:
    """Fetch the total number of countries from the World Bank API and
    construct a URL to request all countries in JSON format."""
    response = get(BASE_COUNTRIES_URL, params={"format": "xml"}, timeout=60)
    content = response.content.decode("utf-8-sig")
    root = ET.fromstring(content)
    # Getting the total countries
    total_countries = int(root.attrib.get("total", "0"))
    countries_url = f"{BASE_COUNTRIES_URL}?format=json&per_page={total_countries}"
    return countries_url

def get_jdbc_options() -> dict:
    """Returns JDBC connection options dictionary for connecting to the
    warehouse Postgres database."""
    jdbc_options = {'host':'warehouse_postgres',
                    'port': '5432', 
                    'dbname' : 'data_warehouse', 
                    'user': 'airflow', 
                    'password' : 'airflow' }
    return jdbc_options

def get_jdbc_url() -> str:
    """Construct and return the JDBC URL string based on JDBC options."""
    jdbc_options = get_jdbc_options()
    return (
    f"jdbc:postgresql://{jdbc_options['host']}:"
    f"{jdbc_options['port']}/{jdbc_options['dbname']}")
