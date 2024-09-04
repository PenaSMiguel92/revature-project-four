import logging
from config.mysql_connection_vars import MYSQL_LOGFILE
class ConnectionFailed(Exception):
    """
        Thrown when connection to database fails because the appropriate .csv file is either missing or contains invalid values.
    """
    def __init__(self, message: str) -> None:
        logging.basicConfig(filename=f"logs/{MYSQL_LOGFILE}.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')
        self.message = '(Connection Failed) : ' + message
        logging.warning(self.message)