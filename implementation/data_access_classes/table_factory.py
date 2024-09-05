from custom_exceptions.table_selection_invalid import TableSelectionInvalidException
from interface.data_access_object_interface import DataAccessObjectInterface
from config.mysql_connection_vars import MYSQL_LOGFILE
import pandas
from pandas import DataFrame
import logging
from mysql.connector import MySQLConnection

sakila_tables: list[str] = ['actor', 'address', 'category', 
                 'city', 'country',  'customer', 
                 'film', 'film_actor', 'film_category', 
                 'film_text', 'inventory', 'language', 
                 'payment', 'rental', 'staff', 'store']

class TableFactory(DataAccessObjectInterface):
    def __init__():
        logging.basicConfig(filename=f"logs/{MYSQL_LOGFILE}.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')
    
    def get_table(self, table_name: str) -> DataFrame:
        if table_name not in sakila_tables:
            TableSelectionInvalidException('Selection is not a Sakila table')

        connection: MySQLConnection = super().get_connection()
        query: str = f'SELECT * FROM {table_name}'
        dataframe: DataFrame = pandas.read_sql(query, connection)

        return dataframe

