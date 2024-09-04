import logging
from config.mysql_connection_vars import MYSQL_LOGFILE

class MenuSelectionInvalidException(Exception):
    """
        Thrown when user input is not within a set of options. 
    """
    def __init__(self, message: str) -> None:
        logging.basicConfig(filename=f"logs/{MYSQL_LOGFILE}.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')
        self.message = "(Invalid Menu Selection) : " + message
        logging.warning(self.message)