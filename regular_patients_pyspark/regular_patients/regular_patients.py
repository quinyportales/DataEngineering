"""This module contains the class PatientsData to modelate 
monthly patient information using Dataframe API from Pyspark"""
from pyspark.sql import DataFrame, SparkSession, DataFrameReader
import pyspark.sql.functions as f
from pyspark.sql.functions import sum as spark_sum, max as spark_max
from pyspark.sql.window import Window
from regular_patients.logger import Log4J


class PatientsData (Log4J) :
    """This class uses spark to load and analizes patient data"""
    def __init__(self, input_data) -> None :
        """Initializes the class and creates the spark session"""
        self.spark : SparkSession = (SparkSession.builder.appName('PatientsData')
            .config('spark.driver.extraJavaOptions',
                    '-Dlog4j.configuration=file:regular_patients/config/log4j.properties')
            .getOrCreate())
        if isinstance(input_data, str):
            self.df_patients: DataFrame = self.load_data(input_data)
        else:
            self.df_patients: DataFrame = input_data
        super().__init__(self.spark)

    def load_data(self, input_data: str) -> DataFrameReader :
        """Loads the CSV data file, inferring the schema"""
        return (self.spark.read
        .format ('csv')
        .option('header', 'true')
        .option('inferschema', 'true')
        .load(input_data))

    def format_date(self, df: DataFrame) -> DataFrame :
        """Takes the effective_date field and tranforms it to a date type"""
        df =  (df.withColumn('effective_from_date_formatted',
                        f.col('effective_from_date').cast('string'))
            .withColumn('effective_from_date_formatted',
                         f.lpad(f.col('effective_from_date_formatted'),  8, '0'))
            .withColumn('effective_from_date_formatted',
                        f.to_date(f.col('effective_from_date_formatted'), 'MMddyyyy')))
        return df.select('patient_id', 'effective_from_date_formatted')

    def filter_by_date_range(self, df: DataFrame, start_date: str, end_date: str) -> DataFrame :
        """Filtering the data by date range"""
        return df.filter(
        (f.col('effective_from_date_formatted') >= f.to_date(f.lit(start_date), 'yyyy-MM-dd')) &
        (f.col('effective_from_date_formatted') <= f.to_date(f.lit(end_date), 'yyyy-MM-dd'))
        )

    def checking_consecutives_records(self, df: DataFrame) -> DataFrame :
        """Identifies consecutive records for each patient based on monthly intervals. 
        This function flags consecutive records by checking if the difference in months 
        between consecutive entries is exactly one. It also calculates the longest sequence 
        of consecutive records per patient"""
        # Defining the window specification
        win_spec = Window.partitionBy('patient_id').orderBy('effective_from_date_formatted')

        # Add previous date column
        df = df.withColumn(
            'prev_date', f.lag(f.col('effective_from_date_formatted')).over(win_spec)
        )
        # Calculate months between current and previous record
        df = df.withColumn(
            'months_between', f.months_between(
                f.col('effective_from_date_formatted'), f.col('prev_date')
                )
        )
        # Flagging the consecutive records
        win_spec_2 = Window.partitionBy('patient_id').orderBy('effective_from_date_formatted')

        df = df.withColumn(
            'is_consecutive', f.when(f.col('months_between') == 1, 1).otherwise(0)
        )
        df = df.withColumn(
            'count_consec', spark_sum(f.col('is_consecutive')).over(win_spec_2)
        )
        # Calculating the maximum consecutive months
        df = (df.withColumn(
            'max_count_consec', spark_max(f.col('count_consec'))
            .over(Window.partitionBy('patient_id'))
        ))
        return df.select('patient_id', 'effective_from_date_formatted',
                         'count_consec', 'max_count_consec')

    def get_result(self, df : DataFrame) -> DataFrameReader:
        """Generates a DataFrame summarizing patient records with flags for long-term continuity.

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
            DataFrame: Processed DataFrame with patient continuity flags"""
        # Selecting unique patient_id and their max consecutive count
        df = df.select('patient_id', 'max_count_consec').distinct()
        # Adding boolean flags for 5, 9, and 11 consecutive months
        df = df.withColumns({
            '5months': f.when(f.col('max_count_consec') >= 5, True).otherwise(False),
            '9months': f.when(f.col('max_count_consec') >= 9, True).otherwise(False),
            '11months': f.when(f.col('max_count_consec') >= 11, True).otherwise(False),
        }).select('patient_id', '5months', '9months', '11months')
        return df

    def run(self, output_path, start_date, end_date):
        """This method runs all the 
        tranformations and write the output file"""

        #instantiating the logger
        self.info('Starting PatientsData')

        # Transforming the date and filtering
        df_formatted = self.format_date(self.df_patients)
        df_filtered = self.filter_by_date_range(df_formatted,start_date, end_date)

        # Checking the intermediate results
        df_filtered.printSchema()
        df_filtered.show(10)

        # Checking the consecutive records
        consecutives = self.checking_consecutives_records(df_filtered)
        consecutives.show(10)

        self.df_patients = self.get_result(consecutives)

        # Saving the resulting dataframe
        self.df_patients.write.mode('overwrite').csv(output_path)

        self.df_patients.show(10)
        self.df_patients.printSchema()
        self.info('Finishing PatientsData')
        # Stopping Spark
        self.spark.stop()
