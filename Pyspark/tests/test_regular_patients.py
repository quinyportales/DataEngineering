'''Test module for PatientsData'''
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType
from pyspark.sql.functions import col, to_date
from regular_patients.regular_patients import PatientsData

END_DATE = '2016-09-30'
START_DATE = '2015-10-01'

@pytest.fixture
def spark():
    '''Fixture to create a spark session for each test'''
    return SparkSession.builder.master("local").appName("test").getOrCreate()

@pytest.fixture
def sample_data(spark):
    '''Test dataframe data'''
    data = [
        (1, 4012016),
        (1, 9012016),
        (2, 9012016),
        (3, 9012016),
        (4, 9012016),
        (1, 8012016),
        (3, 8012016),
        (4, 8012016),
        (1, 7012016),
        (1, 6012016),
        (1, 5012016),
        (2, 3012016),
        (2, 1012016),
        (4, 1012016),
        (3, 8012014),
        (4, 8012018),
        (1, 7012018),
    ]
    schema = 'patient_id STRING, effective_from_date INT'
    return spark.createDataFrame(data, schema)


# Expected output form 'yyyy-MM-dd'
@pytest.fixture
def formatted_date_data (spark):
    '''Test dataframe data'''
    data = [
        (1, '2016-04-01'),
        (1, '2016-09-01'),
        (2, '2016-09-01'),
        (3, '2016-09-01'),
        (4, '2016-09-01'),
        (1, '2016-08-01'),
        (3, '2016-08-01'),
        (4, '2016-08-01'),
        (1, '2016-07-01'),
        (1, '2016-06-01'),
        (1, '2016-05-01'),
        (2, '2016-03-01'),
        (2, '2016-01-01'),
        (4, '2016-01-01'),
        (3, '2014-08-01'),
        (4, '2018-08-01'),
        (1, '2018-07-01'),
    ]
    schema = StructType([
                        StructField('patient_id', StringType()),
                        StructField('effective_from_date_formatted', StringType())
                         ])
    df = spark.createDataFrame(data, schema)
    df =  df.withColumn('effective_from_date_formatted',
                        to_date(col('effective_from_date_formatted')))
    return df

@pytest.fixture
def filtered_data(spark):
    '''Test dataframe data'''
    data = [
        (1, '2016-04-01'),
        (1, '2016-09-01'),
        (2, '2016-09-01'),
        (3, '2016-09-01'),
        (4, '2016-09-01'),
        (1, '2016-08-01'),
        (3, '2016-08-01'),
        (4, '2016-08-01'),
        (1, '2016-07-01'),
        (1, '2016-06-01'),
        (1, '2016-05-01'),
        (2, '2016-03-01'),
        (2, '2016-01-01'),
        (4, '2016-01-01')
    ]
    schema = StructType([
                        StructField('patient_id', StringType()),
                        StructField('effective_from_date_formatted', StringType())
                         ])
    df = spark.createDataFrame(data, schema)
    df =  df.withColumn('effective_from_date_formatted',
                        to_date(col('effective_from_date_formatted')))
    return df

@pytest.fixture
def consecutive_data(spark):
    '''Test dataframe data'''
    data = [
        (1, '2016-04-01', 0, 5),
        (1, '2016-05-01', 1, 5),
        (1, '2016-06-01', 2, 5),
        (1, '2016-07-01', 3, 5),
        (1, '2016-08-01', 4, 5),
        (1, '2016-09-01', 5, 5),
        (2, '2016-01-01', 0, 0),
        (2, '2016-03-01', 0, 0),
        (2, '2016-09-01', 0, 0),
        (3, '2016-08-01', 0, 1),
        (3, '2016-09-01', 1, 1),
        (4, '2016-01-01', 0, 1),
        (4, '2016-08-01', 0, 1),
        (4, '2016-09-01', 1, 1)
    ]
    schema = StructType([
        StructField('patient_id', StringType()),
        StructField('effective_from_date_formatted', StringType()),
        StructField('count_consec', IntegerType(), True),
        StructField('max_count_consec', IntegerType(), True)
    ])
    df = spark.createDataFrame(data, schema)
    df = df.withColumn('effective_from_date_formatted',
                       to_date(col('effective_from_date_formatted')))
    return df

@pytest.fixture
def final_result_data(spark):
    '''Test dataframe data'''
    data = [
        (1, True, False, False),
        (2, False, False, False),
        (3, False, False, False),
        (4, False, False, False)
        ]
    schema = StructType([
        StructField('patient_id', StringType()),
        StructField('5months', BooleanType()),
        StructField('9months', BooleanType()),
        StructField('11months', BooleanType())
        ])
    df = spark.createDataFrame(data, schema)
    return df


@pytest.fixture
def patients_data_instance(mocker, sample_data):
    '''Fixture to create a mock instance of PatientsData.
    Returns: PatientsData- An instance of PatientsData with the mock loaded sample data.'''
    #mocking PatientData.load_data
    mock_load_data = mocker.patch('regular_patients.regular_patients.PatientsData.load_data')
    mock_load_data.return_value = sample_data
    patients_data = PatientsData('sample-path')
    return patients_data

def test_load_data(patients_data_instance, sample_data):
    '''Testing PatientsData.load_data()'''
    assert patients_data_instance.df_patients == sample_data

def test_format_date(patients_data_instance, formatted_date_data):
    '''Testing PatientsData.format_date()'''
    result_df = patients_data_instance.format_date()\
        .select('patient_id', 'effective_from_date_formatted')
    result_data = sorted(result_df.collect())
    expected_data = sorted(formatted_date_data.collect())
    assert result_data == expected_data

def test_filter_by_date_range(patients_data_instance, filtered_data):
    '''Testing PatientsData.filter_by_date_range()'''
    result_df = patients_data_instance.format_date()
    result_df = patients_data_instance.filter_by_date_range(START_DATE, END_DATE)
    result_df = result_df.select('patient_id', 'effective_from_date_formatted')
    result_data = sorted(result_df.collect())
    expected_data = sorted(filtered_data.collect())
    assert result_data == expected_data

def test_checking_consecutives_records(patients_data_instance, consecutive_data):
    '''Testing PatientsData.checking_consecutives_records()'''
    result_df = patients_data_instance.format_date()
    result_df = patients_data_instance.filter_by_date_range(START_DATE, END_DATE)
    result_df = patients_data_instance.checking_consecutives_records()
    result_df = result_df.select('patient_id', 'effective_from_date_formatted',
                                 'count_consec', 'max_count_consec')
    result_data = sorted(result_df.collect())
    expected_data = sorted(consecutive_data.collect())
    assert result_data == expected_data

def test_get_result(patients_data_instance, final_result_data):
    '''Testing PatientsData.get_results()'''
    result_df = patients_data_instance.format_date()
    result_df = patients_data_instance.filter_by_date_range(START_DATE, END_DATE)
    result_df = patients_data_instance.checking_consecutives_records()
    result_df = patients_data_instance.get_result()
    result_data = sorted(result_df.collect())
    expected_data = sorted(final_result_data.collect())
    assert result_data == expected_data
