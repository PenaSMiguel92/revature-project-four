from pyspark.sql import DataFrame as Spark_DF
from interface.input_validation_interface import InputValidation
from interface.menu_interface import MenuInterface
from custom_exceptions.menu_selection_invalid import MenuSelectionInvalidException

from implementation.service_classes.spark_service import SparkService

from enum import Enum

menu_state = Enum('MENU_STATE', [
'INITIAL_STATE',
'WAITING_STATE',
'CLOSING_STATE'
])

class MainMenu(InputValidation, MenuInterface):
    """
        This class will handle the main command line interface (CLI). 
        
        It is a state machine dependent on user input. 
        
        The default state will be initial_state, and depending on user input the current_state will update accordingly. 

        I broke this logic down further into more classes to follow SOLID principles.
    """

    def __init__(self):
        self.current_state = menu_state.INITIAL_STATE
        self.spark_service = None
    
    def set_state(self, state_value: int) -> None:
        self.current_state = state_value
    
    def get_state(self) -> int:
        return self.current_state
    
    def reset_state(self) -> None:
        """
            This is an encapsulated method that should only be accessible by this class.

            There's only so much DRY can do, I still need to call this method at the end of every menu option method.
        """
        self.current_state = menu_state.INITIAL_STATE

    def close_connections(self) -> None:
        if self.spark_service != None:
            self.spark_service.close_connections()

    def display(self) -> None:
        self.current_state = menu_state.WAITING_STATE
        if self.spark_service == None:
            self.spark_service = SparkService()
        
        print('Welcome to the Sakila Database CLI.')
        print('Please select an option:')
        print('A. Display all tables in the Sakila database.')
        print('B. Display the number of distinct actor last names.')
        print('C. Display the non-repeated last names.')
        print('D. Display the repeated last names.')
        print('E. Display the average running time of films.')
        print('F. Display the average running time of films by category.')
        print('G. Enter custom query.')
        print('H. Exit the program.')
        user_input = input('>> ').upper()
        if self.validate_input(user_input, char_input=True, valid_input = 'ABCDEFGH'):
            df: Spark_DF = None
            match(user_input):
                case 'A':
                    sakila_tables = self.spark_service.get_tables()
                    for table in sakila_tables:
                        print(table)

                    self.reset_state()
                case 'B':
                    df = self.spark_service.distinct_actor_lastnames_count_query()
                    self.reset_state()
                case 'C':
                    df = self.spark_service.nonrepeated_lastname_query()
                    self.reset_state()
                case 'D':
                    df = self.spark_service.repeated_lastname_query()
                    self.reset_state()
                case 'E':
                    df = self.spark_service.average_running_time_query()
                    self.reset_state()
                case 'F':
                    df = self.spark_service.average_running_time_by_category_query()
                    self.reset_state()
                case 'G':
                    user_query = input('Enter your query: ')
                    df = self.spark_service.execute_query(user_query)
                    self.reset_state()
                case 'H':
                    self.close_connections()
                    self.set_state(menu_state.CLOSING_STATE)
                case _:
                    raise MenuSelectionInvalidException('Invalid selection')
            
            if df != None:
                df.show(1000, False)
        
        return
        
    def run(self) -> None:
        match self.current_state:
            case menu_state.INITIAL_STATE:
                self.display()
            # case menu_state.ACCOUNT_SUBMENU_STATE:
            #     self.account_submenu()
            # case menu_state.ADMIN_SUBMENU_STATE:
            #     self.admin_submenu()
            # case menu_state.PATIENT_SUBMENU_STATE:
            #     self.patient_submenu()
            # case menu_state.DOCTOR_SUBMENU_STATE:
            #     self.doctor_submenu()
            
