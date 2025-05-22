"""Test module for Countries_Data  functions."""
import pytest
from unittest.mock import MagicMock, patch
from pyspark.testing.utils import assertDataFrameEqual
from src.countries_data import Countries_Data
from test.test_data import spark, raw_countries_data_api , raw_countries_df, countries_df


@pytest.fixture
def countries_data_instance():
    """Fixture that returns a Countries_Data instance """
    return Countries_Data('https://mock-api.worldbank.org/v2/country?format=json')

def test_clean_column_names(countries_data_instance):
    """
    Test Countries_Data.clean_column_names 
    """
    df = countries_data_instance.transform_to_df(spark, raw_countries_data_api)
    result_df = countries_data_instance.clean_column_names(df)
    assertDataFrameEqual(result_df, raw_countries_df)

def test_countries_cast_cols(countries_data_instance):
    """
    Test Countries_Data.countries_cast_cols
    """
    df = countries_data_instance.transform_to_df(spark, raw_countries_data_api)
    df = countries_data_instance.clean_column_names(df)
    result_df = countries_data_instance.countries_cast_cols(df)
    assertDataFrameEqual(result_df, countries_df)