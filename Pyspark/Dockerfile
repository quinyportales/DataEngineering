FROM bitnami/spark:latest

# Añadir PYTHONPATH and workdirectory
ENV PYTHONPATH="${PYTHONPATH}:/Pyspark"
WORKDIR /Pyspark


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


RUN mkdir -p /Pyspark/regular_patients/output && chmod -R 777 /Pyspark/regular_patients/output
RUN mkdir -p /Pyspark/regular_patients/input && chmod -R 777 /Pyspark/regular_patients/input


COPY . .


COPY regular_patients/config/log4j.properties /Pyspark/regular_patients/config/log4j.properties

# Ejecutar el script principal
CMD ["python", "-m", "regular_patients.main"]
