FROM bitnami/spark:latest

# Definir el directorio de trabajo
WORKDIR /Pyspark

# Copiar dependencias primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Eliminar y recrear directorio de salida sin cambiar permisos
RUN rm -rf /Pyspark/regular_patients/output && \
    mkdir -p /Pyspark/regular_patients/output

# Definir el comando por defecto para ejecutar main.py
CMD ["python", "regular_patients/main.py"]
#CMD ["bash", "-c", "python /Pyspark/regular_patients/main.py && tail -f /dev/null"]
