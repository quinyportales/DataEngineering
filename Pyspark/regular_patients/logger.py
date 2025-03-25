"""This module provides a logging utility for PySpark applications using Log4J"""
from pyspark.sql import SparkSession
from py4j.java_gateway import JavaObject

class Log4J:
    """This class facilitates logging messages at different levels (info, debug, 
    warning, and error)"""
    def __init__(self, spark: SparkSession) -> None:
        """Initializes the class"""
        log4j : JavaObject  = spark._jvm.org.apache.log4j
        self.logger : JavaObject = log4j.LogManager.getLogger('RegularPatientsApp')

    def warn(self, message : str)  -> None :
        """Logs warning messages"""
        self.logger.warning(message)

    def error(self, message : str)  -> None :
        """Logs error messages"""
        self.logger.error(message)

    def debug(self, message : str)  -> None :
        """Logs debug messages"""
        self.logger.debug(message)

    def info(self, message : str)  -> None :
        """Logs informational messages"""
        self.logger.info(message)
