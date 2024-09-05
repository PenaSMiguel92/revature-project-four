from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from implementation.data_access_classes.table_factory import TableFactory
from pandas import DataFrame

spark = SparkSession.builder.appName("MySQLDBtoSparkDF").getOrCreate()
spark.conf.set("spark.sql.execution.arrow.enabled", "true")
factory = TableFactory()

film_pdf: DataFrame = factory.get_table('film')

spark.createDataFrame(film_pdf.astype(str)).show()
