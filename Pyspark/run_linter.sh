#!/bin/bash
python -m pylint regular_patients/main.py || python -m pylint regular_patients/regular_patients.py
