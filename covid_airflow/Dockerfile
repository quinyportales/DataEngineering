FROM apache/airflow:2.6.1-python3.9

ENV PYTHONPATH="/opt/airflow"

USER root

# Instala Java y wget, y limpia caché
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Define JAVA_HOME correctamente
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Crea el directorio para los jars y los descarga
RUN mkdir -p /opt/airflow/jars && \
    wget -P /opt/airflow/jars https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/hadoop-aws-3.3.1.jar && \
    wget -P /opt/airflow/jars https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.901/aws-java-sdk-bundle-1.11.901.jar && \
    wget -P /opt/airflow/jars https://jdbc.postgresql.org/download/postgresql-42.7.3.jar

# Copia el entrypoint y da permisos
COPY entrypoint.sh /opt/airflow/entrypoint.sh
RUN chmod +x /opt/airflow/entrypoint.sh

USER airflow

# Instala dependencias Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

EXPOSE 8080

ENTRYPOINT ["/opt/airflow/entrypoint.sh"]
CMD ["webserver"]
