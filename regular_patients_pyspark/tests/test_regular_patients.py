"""Test module for PatientsData"""
import pytest
from unittest.mock import MagicMock, patch
from pyspark.testing.utils import assertDataFrameEqual
from regular_patients.regular_patients import PatientsData
from tests.data_for_testing import END_DATE, START_DATE, sample_data,formatted_date_data, filtered_data, consecutive_data, final_result_data

@pytest.fixture
@patch('regular_patients.regular_patients.SparkSession')
def test_patients_data_instance(mock_spark_session):
    mock_spark = MagicMock()
    mock_spark_session.builder.appName.return_value.config.return_value.getOrCreate.return_value = mock_spark
    return PatientsData('dummy_path')

def test_format_date(test_patients_data_instance):
    """Testing PatientsData.format_date()"""
    result_df =test_patients_data_instance.format_date(sample_data)
    assertDataFrameEqual(result_df, formatted_date_data)

def test_filter_by_date_range(test_patients_data_instance):
    """Testing PatientsData.filter_by_date_range()"""
    result_df = test_patients_data_instance.filter_by_date_range(formatted_date_data, START_DATE, END_DATE)
    assertDataFrameEqual(result_df, filtered_data)
    
def test_checking_consecutives_records(test_patients_data_instance):
    """Testing PatientsData.checking_consecutives_records()"""
    result_df = test_patients_data_instance.checking_consecutives_records(filtered_data)
    assertDataFrameEqual(result_df, consecutive_data)

def test_get_result(test_patients_data_instance):
    """Testing PatientsData.get_results(test_patients_data_instance)"""
    result_df = test_patients_data_instance.get_result(consecutive_data)
    assertDataFrameEqual(result_df, final_result_data)