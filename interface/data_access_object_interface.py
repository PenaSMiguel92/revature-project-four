from abc import ABC
import logging
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from custom_exceptions.connection_failed import ConnectionFailed
from config.mysql_connection_vars import MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_LOGFILE

class DataAccessObjectInterface(object):

    current_connection: MySQLConnection = None
    current_cursor: MySQLCursor = None

    def __init__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataAccessObjectInterface, cls).__new__(cls)
        return cls.instance

    @classmethod
    def get_cursor(class_pointer) -> MySQLCursor:
        """
            This method should be called from child class as super().get_cursor() which will in turn 
            call get_connection, and ensure that only one connection object and one cursor object are created.
        """
        logging.basicConfig(filename=f"logs/{MYSQL_LOGFILE}.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')
        class_pointer.get_connection()
        if class_pointer.current_connection == None:
            raise ConnectionFailed("Please make sure that the python module 'mysql_connection_vars.py' exists.")

        if class_pointer.current_cursor == None:
            try:
                class_pointer.current_cursor = class_pointer.current_connection.cursor()
            except (mysql.connector.ProgrammingError, ValueError) as mysql_error:
                logging.error(mysql_error.msg)
                return
            logging.info("Connected to database successfully.")
        
        return class_pointer.current_cursor
    
    @classmethod
    def get_connection(class_pointer) -> MySQLConnection:
        """
            Make sure to have a python module with MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, and MYSQL_LOGFILE 
            variables defined in a directory called config/
        """
        
        try:
            if class_pointer.current_connection == None:
                logging.info('Attempting to connect...')
                class_pointer.current_connection = mysql.connector.connect(user=MYSQL_USERNAME, password=MYSQL_PASSWORD, host=MYSQL_HOST, \
                                                                           database=MYSQL_DATABASE, port=MYSQL_PORT)
            
        except IOError as error:
            print(f"(I/O Error): {error.strerror}")
            print("Please make sure that the specified python module exists.")
            return
        except mysql.connector.Error as msql_error:
            print(f"(Error connecting to database): {msql_error.msg}")
            logging.warning('Connection to MySQL failed, please make sure python module exists in config folder with correct variable values.')
            if class_pointer.current_connection != None:
                class_pointer.current_connection.close()
                class_pointer.current_connection = None
            return

        return class_pointer.current_connection        

    @classmethod
    def commit_changes(class_pointer) -> None:
        class_pointer.current_connection.commit()
        logging.info('Changes were commited to the database.')

    @classmethod
    def close_connection(class_pointer) -> bool:
        if class_pointer.current_cursor != None:
            class_pointer.current_cursor.close()
            class_pointer.current_cursor = None
        if class_pointer.current_connection != None:
            class_pointer.current_connection.close()
            class_pointer.current_connection = None
            logging.info("Database connection closed.")
        return True
    