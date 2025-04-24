"""Test dataframe data"""
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, LongType, IntegerType, DateType
from unittest.mock import MagicMock, patch


END_DATE = '2016-09-30'
START_DATE = '2015-10-01'

spark = SparkSession.builder.master('local').appName('test').getOrCreate()


def string_to_date(data):
    return(data[0], datetime.strptime(data[1], '%Y-%m-%d').date())

sample_data = spark.createDataFrame([
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
        (1, 7012018),], 
        StructType([StructField('patient_id', StringType()), StructField('effective_from_date', IntegerType())]))


# Expected output form 'yyyy-MM-dd'
formatted_date_data =  [(1, '2016-04-01'),
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
        (1, '2018-07-01'),]

formatted_date_data_schema = ( StructType([
                    StructField('patient_id', StringType()),
                    StructField('effective_from_date_formatted', DateType())]))

formatted_date_data = list(map(string_to_date, formatted_date_data))
formatted_date_data = spark.createDataFrame(formatted_date_data, formatted_date_data_schema)

filtered_data= [(1, '2016-04-01'),
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
        (4, '2016-01-01')]
filtered_data_schema =  ( StructType([StructField('patient_id', StringType()),
                StructField('effective_from_date_formatted', DateType())]))
filtered_data = list(map(string_to_date, filtered_data))
filtered_data = spark.createDataFrame(filtered_data, filtered_data_schema)


consecutive_data = [   
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
        (4, '2016-09-01', 1, 1)]

consecutive_data_schema = StructType (
        [StructField('patient_id', StringType()),
        StructField('effective_from_date_formatted', DateType()),
        StructField('count_consec', LongType(), True),
        StructField('max_count_consec', LongType(), True)])

def string_to_date(data):
    return(data[0], datetime.strptime(data[1], '%Y-%m-%d').date(), data[2], data[3])
consecutive_data = list(map(string_to_date, consecutive_data))
consecutive_data = spark.createDataFrame(consecutive_data, consecutive_data_schema)


final_result_data= spark.createDataFrame(
        [(1, True, False, False),
        (2, False, False, False),
        (3, False, False, False),
        (4, False, False, False)], 
        StructType([
            StructField('patient_id', StringType()),
            StructField('5months', BooleanType()),
            StructField('9months', BooleanType()),
            StructField('11months', BooleanType())
        ]))