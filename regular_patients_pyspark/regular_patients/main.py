"""This module implements the PatientsData class to analyze the regular patient data"""
from pathlib import Path
from regular_patients import PatientsData

if __name__ == '__main__':
    current_directory = Path(__file__).parent
    INPUT_PATH = str(current_directory / 'input' / 'enroll.csv')
    OUTPUT_PATH = str(current_directory / 'output')
    START_DATE = '2015-10-01'
    END_DATE = '2016-09-30'

    patients = PatientsData(INPUT_PATH)
    #tranforming, filtering and writting the final result
    patients.run(OUTPUT_PATH, START_DATE, END_DATE)
