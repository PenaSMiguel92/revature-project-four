from custom_exceptions.username_invalid import UsernameInvalid
from custom_exceptions.password_invalid import PasswordInvalid
from custom_exceptions.profile_invalid import ProfileInvalid
from custom_exceptions.balance_invalid import BalanceInvalid

from interface.input_validation_interface import InputValidation
from interface.account_service_interface import AccountServiceInterface
from custom_exceptions.account_menu_selection_invalid import AccountMenuSelectionInvalid
from implementation.data_access_classes.account_dao import AccountDAO
from implementation.data_model_classes.account import Account

from mysql.connector import Error
from enum import Enum

import logging

account_service_state = Enum('ACCOUNT_STATE', [
    'INITIAL_STATE',
    'CREATING_USER_STATE',
    'LOADING_USER_STATE',
    'LOADED_USER_STATE',
    'CLOSING_STATE'
])

class AccountService(InputValidation, AccountServiceInterface):

    def __init__(self) -> None:
        logging.basicConfig(filename="logs/rxbuddy_database.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')
        self.current_state = account_service_state.INITIAL_STATE
        self.account_dao: AccountDAO = AccountDAO()
        self.current_account: Account = None

    def account_login(self) -> None:
        print('\nPlease enter your username: ')
        while self.current_account == None:
            try:
                username = input('>>>').lower()
                self.current_account = self.account_dao.get_account_by_username(username)
                break
            except Error as mysql_error:
                print('Username does not exist. Please enter a valid username.')
                logging.warning('User attempted to login with invalid credentials.')

        if self.current_account == None:
            print('Username does not exist. Please enter a valid username.')
            logging.warning('User attempted to login with invalid credentials.')
            self.current_state = account_service_state.INITIAL_STATE
            return False
        
        print('\nPlease enter your password: ')
        retries = 3
        while retries > 0:
            user_password = input('>>>')
            if self.current_account.accountPassword != user_password:
                print(f"Passwords do not match, please try again ({retries - 1})")
                retries -= 1
            else:
                break

        if retries == 0:
            print('Too many attempts. Try again later.')
            logging.warning('User attempted to login with invalid credentials.')
            self.current_account = None
            self.current_state = account_service_state.INITIAL_STATE
            return False
        
        self.account_greeting()
        self.current_state = account_service_state.LOADED_USER_STATE
        return True
    
    def account_greeting(self) -> None:
        if self.current_account == None:
            return 
        
        print(f'\nWelcome back {self.current_account.firstName} {self.current_account.lastName}!')

    def account_register(self) -> None:
        # while self.current_account == None: 
        username_input = ''
        pasword_input = ''
        firstname_input = ''
        lastname_input = ''
        balance_input: float = 0.00 

        while True:
            try:
                print('Please enter a username: ')
                username_input = input('>>>').lower()
                if not self.validate_input(username_input, credential_input=True):
                    raise UsernameInvalid('Username must not contain whitespace, must be longer than 4 characters, and have some numbers.')
                
                check_existing = self.account_dao.get_account_by_username(username_input)
                if check_existing != None:
                    raise UsernameInvalid('That username is already taken! Please try again.')
                
                break
            except UsernameInvalid as err:
                print(err.message)
        
        while True:
            try:
                print('Please enter a password: ')
                password_input = input('>>>')
                print('Please reenter that password: ')
                password_input_2 = input('>>>')
                if password_input != password_input_2:
                    raise PasswordInvalid('Passwords do not match.')
                
                if not self.validate_input(password_input, credential_input=True):
                    raise PasswordInvalid('Password must have more than 4 characters and have no whitespace.')
                
                break
            except PasswordInvalid as err:
                print(err.message)

        while True:
            try:
                print('Please enter your first name: ')
                firstname_input = input('>>>')
                if not self.validate_input(firstname_input, string_input=True):
                    raise ProfileInvalid('First name must have more than 2 characters and be alphabetical.')
                
                print('Please enter your last name: ')
                lastname_input = input('>>>')
                if not self.validate_input(lastname_input, string_input=True):
                    raise ProfileInvalid('First name must have more than 2 characters and be alphabetical.')

                break
            except ProfileInvalid as err:
                print(err.message)

        while True:
            try:
                print('How much will you deposit into your account? ')
                balance_input = input('>>>')
                if not self.validate_input(balance_input, integer_input=True):
                    raise BalanceInvalid('Please enter a number.')
                if float(balance_input) > 1000:
                    raise BalanceInvalid('Please enter less than $1,000.')
                break
            except BalanceInvalid as err:
                print(err.message)
        try:
            new_account = Account(0, username_input, password_input, firstname_input, lastname_input, balance_input, 2)
            self.current_account = self.account_dao.create_account(new_account)
        except Error as mysql_error:
            logging.error(f'Failed to create an account and save to database. {mysql_error.msg}')

        if self.current_account == None:
            self.current_state = account_service_state.INITIAL_STATE
            return False
        
        print('Account successfully created!')
        self.current_state = account_service_state.LOADED_USER_STATE
        return True
    
    def display(self) -> bool:
        print('\nWould you like to register a new user or login?')
        print('(R)egister')   
        print('(L)ogin') 
        print('(E)xit')
        while self.current_state == account_service_state.INITIAL_STATE:
            try: 
                user_input = input('>>>').upper()
                if not self.validate_input(user_input, char_input = True, valid_input = 'RLE'):
                    raise AccountMenuSelectionInvalid("Please choose a valid menu option.")
                self.process_input(user_input)

            except AccountMenuSelectionInvalid as msg:
                print(msg.message)

        return True

    def process_input(self, input: str) -> None:
        match (input):
            case 'R':
                self.current_state = account_service_state.CREATING_USER_STATE
            case 'L':
                self.current_state = account_service_state.LOADING_USER_STATE
            case 'E':
                self.current_state = account_service_state.CLOSING_STATE

    def close_connections(self) -> bool:
        """
            This method closes connections if they exist.
        """
        if self.account_dao.current_connection != None:
            self.account_dao.close_connection()
    
    def set_state(self, state: int) -> None:
        self.current_state = state
    
    def get_state(self) -> int:
        return self.current_state
    
    def get_account_role(self) -> bool:
        return self.current_account.roleName

    def run(self) -> bool:
        match self.current_state:
            case account_service_state.INITIAL_STATE:
                return self.display()
            case account_service_state.CREATING_USER_STATE:
                return self.account_register()
            case account_service_state.LOADING_USER_STATE:
                return self.account_login()
            case account_service_state.LOADED_USER_STATE:
                return True
            case account_service_state.CLOSING_STATE:
                return True