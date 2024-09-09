from pyspark.sql import SparkSession
from implementation.data_access_classes.table_factory import TableFactory
from pandas import DataFrame

spark = SparkSession.builder.appName("MySQLDBtoSparkDF").getOrCreate()
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
factory = TableFactory()

film_pdf: DataFrame = factory.get_table('film')

spark.createDataFrame(film_pdf).show()
