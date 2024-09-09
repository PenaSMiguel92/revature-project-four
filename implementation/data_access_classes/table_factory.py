from custom_exceptions.table_selection_invalid import TableSelectionInvalidException
from interface.data_access_object_interface import DataAccessObjectInterface
from config.mysql_connection_vars import MYSQL_LOGFILE
import pandas
from pandas import DataFrame
import logging
from mysql.connector.cursor import MySQLCursor

sakila_tables: list[str] = ['actor', 'address', 'category', 
                 'city', 'country',  'customer', 
                 'film', 'film_actor', 'film_category', 
                 'film_text', 'inventory', 'language', 
                 'payment', 'rental', 'staff', 'store']

class TableFactory(DataAccessObjectInterface):
    def __init__(self):
        logging.basicConfig(filename=f"logs/{MYSQL_LOGFILE}.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')
    
    def get_table(self, table_name: str) -> DataFrame:
        '''
            This method will return a Pandas DataFrame for a given table. The table name must be a Sakila table.
        '''
        table_name = table_name.lower()
        if table_name not in sakila_tables:
            TableSelectionInvalidException('Selection is not a Sakila table')

        cursor: MySQLCursor = super().get_cursor()
        query: str = f'SELECT * FROM {table_name}'
        cursor.execute(query)

        dataframe: DataFrame = pandas.DataFrame(cursor.fetchall())
        dataframe.columns = cursor.column_names

        return dataframe

