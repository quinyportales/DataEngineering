"""Data to be used in the unit test module"""
from datetime import datetime, date
import pytest
from unittest.mock import patch, MagicMock
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DateType, IntegerType, FloatType
import pyspark.sql.functions as f


@pytest.fixture
def spark_session_mock():
    mock_spark = MagicMock(name="SparkSessionMock")
    with patch('config_covid.config_covid.spark_session') as mock_context_mgr:
        mock_context_mgr.return_value.__enter__.return_value = mock_spark
        mock_context_mgr.return_value.__exit__.return_value = None
        yield mock_spark

@pytest.fixture
def minio_client_mock():
    mock_minio = MagicMock(name="Minion_Handler_Mock")
    mock_minio.upload_minio = MagicMock()
    mock_minio.fetch_df_from_minio = MagicMock()
    
    with patch('config_covid.config_covid.get_minio_client', return_value=mock_minio):
        yield mock_minio

spark = SparkSession.builder.master('local').appName('test').getOrCreate()



covid_api_data = [{"Active Cases_text":"","Country_text":"World","Last Update":"2025-05-21 11:54",
                   "New Cases_text":"7,010,681","New Deaths_text":"90,413","Total Cases_text":"704,753,890",
                   "Total Deaths_text":"675,619,811","Total Recovered_text":"899.4"},
                {"Active Cases_text":"334,805,269","Country_text":"USA","Last Update":"2025-05-21 11:54",
                   "New Cases_text":"1,219,487","New Deaths_text":"333,985","Total Cases_text":"111,820,082",
                   "Total Deaths_text":"109,814,428","Total Recovered_text":"3,642"},
                {"Active Cases_text":"11,668,278","Country_text":"Belgium","Last Update":"2025-05-21 10:54",
                    "New Cases_text":"34,376","New Deaths_text":"416,659","Total Cases_text":"4,861,695",
                    "Total Deaths_text":"4,826,798","Total Recovered_text":"2,946"}]

countries_api_data = [{
                "page": 1,
                "pages": 6,
                "per_page": "50",
                "total": 296
            },
                [{"id": "ABW",
                "iso2Code": "AW",
                "name": "Aruba",
                "region": {"id": "LCN", "iso2code": "ZJ", "value": "Latin America & Caribbean"},
                "adminregion": {"id": "", "iso2code": "", "value": ""},
                "incomeLevel": {"id": "HIC", "iso2code": "XD", "value": "High income"},
                "lendingType": {"id": "LNX", "iso2code": "XX", "value": "Not classified"},
                "capitalCity": "Oranjestad",
                "longitude": "-70.0167",
                "latitude": "12.5167"},
                {"id": "AFE",
                "iso2Code": "ZH",
                "name": "Africa Eastern and Southern",
                "region": {"id": "NA", "iso2code": "NA", "value": "Aggregates"},
                "adminregion": {"id": "", "iso2code": "", "value": ""},
                "incomeLevel": {"id": "NA", "iso2code": "NA", "value": "Aggregates"},
                "lendingType": {"id": "", "iso2code": "", "value": "Aggregates"},
                "capitalCity": "",
                "longitude": "",
                "latitude": ""},
                {"id": "AFG",
                "iso2Code": "AF",
                "name": "Afghanistan",
                "region": {"id": "SAS", "iso2code": "8S", "value": "South Asia"},
                "adminregion": {"id": "SAS", "iso2code": "8S", "value": "South Asia"},
                "incomeLevel": {"id": "LIC", "iso2code": "XM", "value": "Low income"},
                "lendingType": {"id": "IDX", "iso2code": "XI", "value": "IDA"},
                "capitalCity": "Kabul",
                "longitude": "69.1761",
                "latitude": "34.5228"}
                ]]

raw_covid_schema = StructType([
    StructField('country_name', StringType(), True),
    StructField('active_cases', StringType(), True),
    StructField('last_update', StringType(), True),
    StructField('new_cases', StringType(), True),
    StructField('new_deaths', StringType(), True),
    StructField('total_cases', StringType(), True),
    StructField('total_deaths', StringType(), True),
    StructField('total_recovered', StringType(), True),
    StructField('ingested_date', DateType(), True),
])

raw_covid_data = [
    ('World', '', "2025-05-21 11:54",
     "7,010,681", "90,413", "704,753,890", "675,619,811", "899.4", date.today()),

    ('USA', "334,805,269", "2025-05-21 11:54",
     "1,219,487", "333,985", "111,820,082", "109,814,428","3,642", date.today()),

    ('Belgium', "11,668,278", "2025-05-21 10:54",
     "34,376", "416,659", "4,861,695", "4,826,798", "2,946", date.today())
]

raw_covid_df = spark.createDataFrame(raw_covid_data, schema=raw_covid_schema)

covid_schema = StructType([
    StructField('country_name', StringType(), True),
    StructField('active_cases', IntegerType(), True),
    StructField('last_update', DateType(), True),
    StructField('new_cases', IntegerType(), True),
    StructField('new_deaths', IntegerType(), True),
    StructField('total_cases', IntegerType(), True),
    StructField('total_deaths', IntegerType(), True),
    StructField('total_recovered', FloatType(), True),
    StructField('ingested_date', DateType(), False),
])

covid_data = [
    ('World', None, datetime.strptime('2025-05-21', '%Y-%m-%d').date(),
     7010681, 90413, 704753890, 675619811, 899.4, date.today()),

    ('USA', 334805269, datetime.strptime('2025-05-21', '%Y-%m-%d').date(),
     1219487, 333985, 111820082, 109814428, 3642.0, date.today()),

    ('Belgium', 11668278, datetime.strptime('2025-05-21', '%Y-%m-%d').date(),
     34376, 416659, 4861695, 4826798, 2946.0, date.today())
]
covid_expected_df = spark.createDataFrame(covid_data, schema=covid_schema)

raw_countries_data_api = [
    {
        "id": "ABW",
        "name": "Aruba",
        "region": {"id": "ABW", "value": "Latin America & Caribbean"},
        "incomeLevel": {"id": "HIC", "value": "High income"}
    },
    {
        "id": "AFE",
        "name": "Africa Eastern and Southern",
        "region": {"id": "AFE", "value": "Aggregates"},
        "incomeLevel": {"id": "NA", "value": "Aggregates"}
    },

    {
        "id": "AFG",
        "name": "Afghanistan",
        "region": {"id": "AFE", "value": "South Asia"},
        "incomeLevel": {"id": "NA", "value": "Low income"}
    }
]

raw_countries_schema = StructType(
    [StructField("country_id", StringType(), True),
    StructField("country_name", StringType(), True),
    StructField("region", StringType(), True),
    StructField("income_level", StringType(), True),
    StructField('ingested_date', DateType(), False)]
    )

raw_countries_data = [
    ("ABW",  "Aruba", "Latin America & Caribbean", "High income", date.today()),
    ("AFE",  "Africa Eastern and Southern", "Aggregates", "Aggregates", date.today()),
    ("AFG",  "Afghanistan", "South Asia", "Low income", date.today() )
]
raw_countries_df = spark.createDataFrame(raw_countries_data, schema=raw_countries_schema)


countries_df = raw_countries_df.withColumn(
    'ingested_year_month',
    f.date_format(f.col('ingested_date'), 'yyyy/MM')
)

countries_schema = StructType([
        StructField("country_id", StringType(), True),
        StructField("country_name", StringType(), True),
        StructField("region", StringType(), True),
        StructField("income_level", StringType(), True),
        StructField("ingested_date", DateType(), False),
    ])



today = date.today()
last_update = datetime.strptime('2025-05-21', '%Y-%m-%d').date()

duplicated_null_data_covid = [
        ('USA', 334805269, last_update, 1219487, 333985, 111820082, 109814428, 3642.0, today),
        ('USA', 334805269, last_update, 1219487, 333985, 111820082, 109814428, 3642.0, today),  #duplicated
        ('Belgium', 11668278, last_update, 34376, 416659, 4861695, 4826798, 2946.0, today),
        ('World', None, last_update, 7010681, 90413, 704753890, 675619811, 899.4, today),  # null
    ]
duplicated_null_covid_df =  spark.createDataFrame(duplicated_null_data_covid, schema=covid_schema)

duplicated_null_data_countries = [
        ("ABW", "Aruba", "Latin America & Caribbean", "High income", today),
        ("ABW", "Aruba", "Latin America & Caribbean", "High income", today),  #duplicated
        ("AFE", "Africa Eastern and Southern", "Aggregates", "Aggregates", today),
        ("AFG", "Afghanistan", "South Asia", "Low income", today),
        ("AFG", None, "South Asia", "Low income", today),  #null
    ]

duplicated_null_countries_df = spark.createDataFrame(duplicated_null_data_countries, schema=countries_schema)