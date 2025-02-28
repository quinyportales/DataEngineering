## Description
Task 3. Find regular patients 

## Execution Instructions

### 1. Prepare Permissions to Run the Linter
```bash
chmod +x run_linter.sh

### 2. Start the Environment with Docker
docker-compose up -d

### 3. View Results
docker-compose logs -f pyspark/linter/tests

## Project Structure
/pyspark: Contains the code for the task using Apache Spark with PySpark.
/linter: Files for the linter that checks the code style.
/tests: Files containing unit tests 