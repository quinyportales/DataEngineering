FROM bitnami/spark:latest

# Variables de entorno
ENV PYARROW_IGNORE_TIMEZONE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/regular_patients_pyspark"


# Directorio de trabajo
WORKDIR /regular_patients_pyspark

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear directorios de entrada/salida
USER root
RUN mkdir -p /regular_patients_pyspark/regular_patients/input \
             /regular_patients_pyspark/regular_patients/output \
    && chmod -R 777 /regular_patients_pyspark/regular_patients

# Copiar código fuente
COPY . .

# Copiar configuración específica
COPY regular_patients/config/log4j.properties /regular_patients_pyspark/regular_patients/config/log4j.properties

# Comando por defecto
CMD ["python", "-m", "regular_patients.main"]
