"""Test module for Covid_Data  functions."""
import pytest
from unittest.mock import MagicMock, patch
from pyspark.testing.utils import assertDataFrameEqual
from src.covid_data import Covid_Data
from test.test_data import spark, raw_covid_df,covid_api_data,covid_expected_df


@pytest.fixture
def covid_data_instance():
    """Fixture that returns an Covid_Data  instance """
    return Covid_Data('https://mock-covid-19.dataflowkit.com/v1')


def test_clean_column_names(covid_data_instance):
    """
    TestCovid_Data.clean_column_names 
    """
    df = covid_data_instance.transform_to_df(spark,covid_api_data)
    df = df[1]
    result_df = covid_data_instance.clean_column_names(df)
    assertDataFrameEqual(result_df, raw_covid_df)

def test_covid_cast_cols(covid_data_instance):
    """
    TestCovid_Data.covid_cast_cols
    """
    df =covid_data_instance.transform_to_df(spark,covid_api_data)
    df = covid_data_instance.clean_column_names(df)
    result_df = covid_data_instance.covid_cast_cols(df)
    assertDataFrameEqual(result_df, covid_expected_df)
