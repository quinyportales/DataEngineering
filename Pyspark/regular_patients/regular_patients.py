'''This module contains the class PatientsData to modelate 
monthly patient information using Dataframe API from Pyspark'''
from  pyspark.sql import DataFrame
from pyspark.sql import SparkSession, DataFrameReader
from pyspark.sql.functions import col, lit, lpad, to_date, lag, months_between, when
from pyspark.sql.functions import sum as spark_sum, max as spark_max
from pyspark.sql.window import Window

class PatientsData :
    'This class uses spark to load and analizes patient data'
    def __init__(self, file_path: str) -> None :
        '''Initializes the class from a CSV file and creates the spark session 
        Parameters:
        file_path : CSV data file path
        '''
        self.spark = SparkSession.builder.appName("PatientsData").getOrCreate()
        self.df_patients = self.load_data(file_path)

    def load_data(self, file_path: str) -> DataFrameReader :
        'Loads the CSV data file, inferring the schema'
        return self.spark.read\
        .format ('csv')\
        .option('header', 'true')\
        .option('inferschema', 'true')\
        .load(file_path)

    def format_date(self) -> DataFrame :
        '''Takes the effective_date field and tranforms it to a date type'''
        self.df_patients = self.df_patients\
            .withColumn('effective_from_date_formatted', \
                        col('effective_from_date').cast('string'))\
            .withColumn('effective_from_date_formatted', \
                         lpad(col('effective_from_date_formatted'),  8, '0')) \
            .withColumn('effective_from_date_formatted', \
                        to_date(col('effective_from_date_formatted'), 'MMddyyyy'))
        return self.df_patients

    def filter_by_date_range(self, start_date: str, end_date: str) -> DataFrame :
        '''Filtering the data by date range'''
        self.df_patients = self.df_patients.filter(
        (col("effective_from_date_formatted") >= to_date(lit(start_date), 'yyyy-MM-dd')) &
        (col("effective_from_date_formatted") <= to_date(lit(end_date), 'yyyy-MM-dd'))
        )
        return self.df_patients

    def checking_consecutives_records(self) -> DataFrame :
        '''Identifies consecutive records for each patient based on monthly intervals. 
        This function flags consecutive records by checking if the difference in months 
        between consecutive entries is exactly one. It also calculates the longest sequence 
        of consecutive records per patient.'''
        # Defining the window specification
        win_spec = Window.partitionBy('patient_id').orderBy('effective_from_date_formatted')

        # Add previous date column
        self.df_patients = self.df_patients.withColumn(
            'prev_date', lag(col('effective_from_date_formatted')).over(win_spec)
        )
        # Calculate months between current and previous record
        self.df_patients = self.df_patients.withColumn(
            'months_between', months_between(col('effective_from_date_formatted'), col('prev_date'))
        )
        # Flagging the consecutive records
        win_spec_2 = Window.partitionBy('patient_id').orderBy('effective_from_date_formatted')

        self.df_patients = self.df_patients.withColumn(
            'is_consecutive', when(col('months_between') == 1, 1).otherwise(0)
        )
        self.df_patients = self.df_patients.withColumn(
            'count_consec', spark_sum(col('is_consecutive')).over(win_spec_2)
        )
        # Calculating the maximum consecutive months
        self.df_patients = self.df_patients.withColumn(
            'max_count_consec', spark_max(col('count_consec'))\
            .over(Window.partitionBy('patient_id'))
        )
        return self.df_patients

    def get_result(self) -> DataFrameReader:
        '''Generates a DataFrame summarizing patient records with flags for long-term continuity.

        This function processes the dataset to identify patients who have maintained 
        continuous records for at least 5, 9, or 11 months. It returns a DataFrame with:
        
        - `patient_id`: Unique identifier for each patient.
        - `5months`: Boolean flag (True/False) indicating if the patient 
            has at least 5 consecutive months.
        - `9months`: Boolean flag (True/False) indicating if the patient 
            has at least 9 consecutive months.
        - `11months`: Boolean flag (True/False) indicating if the patient 
            has at least 11 consecutive months.
        
        Returns:
            DataFrame: Processed DataFrame with patient continuity flags.'''

        # Selecting unique patient_id and their max consecutive count
        self.df_patients = self.df_patients.select('patient_id', 'max_count_consec').distinct()
        # Adding boolean flags for 5, 9, and 11 consecutive months
        self.df_patients = self.df_patients.withColumns({
            '5months': when(col("max_count_consec") >= 5, True).otherwise(False),
            '9months': when(col("max_count_consec") >= 9, True).otherwise(False),
            '11months': when(col("max_count_consec") >= 11, True).otherwise(False),
        }).select('patient_id', '5months', '9months', '11months')
        return self.df_patients
