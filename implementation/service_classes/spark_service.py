from interface.spark_service_interface import SparkServiceInterface
from pyspark.sql import SparkSession, DataFrame as Spark_DF
from custom_exceptions.table_selection_invalid import TableSelectionInvalidException
from implementation.data_access_classes.table_factory import TableFactory, sakila_tables
from pandas import DataFrame as PD_DF


class SparkService(SparkServiceInterface):
    '''
        This class abstracts away the implementation details of working with MySQL and Spark.
        Simply create an object of this class, and call the methods to get the desired Spark DataFrames.
    '''
    def __init__(self):
        self.spark = SparkSession.builder.appName("MySQLDBtoSparkDF").getOrCreate()
        self.spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
        self.factory = TableFactory()
        self.initialize_spark_sql()

    def initialize_spark_sql(self) -> bool:
        for table in sakila_tables:
            table_pdf: PD_DF = self.factory.get_table(table)
            self.spark.createDataFrame(table_pdf).createOrReplaceTempView(table)

        return True
    
    def get_spark(self) -> SparkSession:
        return self.spark
    
    def get_factory(self) -> TableFactory:
        return self.factory
    
    def get_table(self, table_name: str) -> Spark_DF:
        table_name = table_name.lower()
        if table_name not in sakila_tables:
            raise TableSelectionInvalidException('Selection is not a Sakila table')
        
        return self.spark.sql(f'SELECT * FROM {table_name}')

    def get_tables(self) -> list[str]:
        return sakila_tables
    
    def distinct_actor_lastnames_count_query(self) -> Spark_DF:
        df = self.execute_query('SELECT COUNT(DISTINCT last_name) FROM actor')
        df = df.withColumnRenamed('count(DISTINCT last_name)', 'Number of Distinct Lastnames')
        return df
    
    def nonrepeated_lastname_query(self) -> Spark_DF:
        df = self.execute_query('SELECT last_name FROM actor WHERE last_name IN (SELECT last_name FROM actor GROUP BY last_name HAVING COUNT(last_name) = 1)')
        df = df.withColumnRenamed('last_name', 'Non-repeated Last Names')
        return df   
    
    def repeated_lastname_query(self) -> Spark_DF:
        df = self.execute_query('SELECT DISTINCT(last_name) FROM actor WHERE last_name IN (SELECT last_name FROM actor GROUP BY last_name HAVING COUNT(last_name) > 1)')
        df = df.withColumnRenamed('last_name', 'Repeated Last Names')
        return df
    
    def average_running_time_query(self) -> Spark_DF:
        df = self.execute_query('SELECT AVG(length) FROM film')
        df = df.withColumnRenamed('avg(length)', 'Average Running Time')
        return df
    
    def average_running_time_by_category_query(self) -> Spark_DF:
        df = self.execute_query('SELECT category.name, AVG(film.length) FROM category JOIN film_category ON category.category_id = film_category.category_id JOIN film ON film_category.film_id = film.film_id GROUP BY category.name')
        df = df.withColumnRenamed('avg(length)', 'Average Running Time')
        return df

    def execute_query(self, query: str) -> Spark_DF:
        result = self.spark.sql(query)
        return result
    
    def close_connections(self) -> None:
        self.spark.stop()
        self.factory.close_connection()
        return