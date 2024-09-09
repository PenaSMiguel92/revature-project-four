from abc import ABC, abstractmethod
from implementation.data_access_classes.table_factory import TableFactory
from pyspark.sql import SparkSession, DataFrame as Spark_DF
from pandas import DataFrame as PD_DF

class SparkServiceInterface(ABC):
    def initialize_spark_sql(self) -> bool:
        '''
            This method will create a Spark DataFrame for each table in the Sakila database.
            Making them available for querying with Spark SQL.
        '''
        ...
    
    def get_spark(self) -> SparkSession:
        '''
            Getter method for the SparkSession object.
        '''
        ...
    
    
    def get_factory(self) -> TableFactory:
        '''
            Getter method for the TableFactory object.
        '''
        ...
    
    def get_table(self, table_name: str) -> Spark_DF:
        '''
            This method will return a Spark DataFrame for a given table.
        '''
        ...

    def get_tables(self) -> list[str]:
        '''
            This method will return a list of table names in the Sakila database.
        '''
        ...
    
    def distinct_actor_lastnames_count_query(self) -> Spark_DF:
        '''
            This method will return a Spark DataFrame with a count of distinct actor last names.
        '''
        ...
    
    def nonrepeated_lastname_query(self) -> Spark_DF:
        '''
            This method will return a Spark DataFrame with the last name of actors with non-repeated last names.
        '''
        ...  
    
    def repeated_lastname_query(self) -> Spark_DF:
        '''
            This method will return a Spark DataFrame with the last name of actors with repeated last names.
        '''
        ...
    
    def average_running_time_query(self) -> Spark_DF:
        '''
            This method will return a Spark DataFrame with the average running time of films.
        '''
        ...
    
    def average_running_time_by_category_query(self) -> Spark_DF:
        '''
            This method will return a Spark DataFrame with the average running time of films by category.
        '''
        ...

    def execute_query(self, query: str) -> Spark_DF:
        '''
            This method will execute a query on the Spark DataFrame.
            Table names are one to one with the Sakila database tables.
        '''
        ...