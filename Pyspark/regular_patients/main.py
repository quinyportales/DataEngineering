'''This module implements the PatientsData class to analyze the regular patient data'''
from regular_patients import PatientsData

if __name__ == '__main__':
    FILE_PATH = 'regular_patients/input/enroll.csv'
    #creating the spark session and loading the data
    patients = PatientsData(FILE_PATH)

    #tranforming te effective_from_date field to date type
    patients.format_date()

    #filtering by date
    END_DATE = '2016-09-30'
    START_DATE = '2015-10-01'
    patients.filter_by_date_range(START_DATE, END_DATE)
    df_patients = patients.df_patients
    df_patients.printSchema()
    df_patients.show(10)

    #identifying consecutives
    consecutives = patients.checking_consecutives_records()
    consecutives.show(10)

    #getting the continuous records for at least 5, 9, or 11 months Dataframe
    df_patients = patients.get_result()
    df_patients.write.mode('overwrite').option('header', 'true')\
        .csv('regular_patients/output/result.csv')
    df_patients.show(10)
    df_patients.printSchema()
