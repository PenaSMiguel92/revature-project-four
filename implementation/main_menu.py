from interface.input_validation_interface import InputValidation
from interface.menu_interface import MenuInterface
from custom_exceptions.menu_selection_invalid import MenuSelectionInvalidException
# from custom_exceptions.invalid_profile import InvalidProfileException
# from custom_exceptions.data_missing import DataMissingException
# from implementation.profile_handler import ProfileHandler
# from implementation.biostat_handler import BiostatHandler

from implementation.service_classes.account_service import AccountService
from implementation.service_classes.account_service import account_service_state
from implementation.service_classes.admin_service import AdminService
from implementation.service_classes.admin_service import admin_service_state
from implementation.service_classes.doctor_service import DoctorService
from implementation.service_classes.doctor_service import doctor_service_state
from implementation.service_classes.patient_service import PatientService
from implementation.service_classes.patient_service import patient_service_state

from enum import Enum

menu_state = Enum('MENU_STATE', [
'INITIAL_STATE',
'WAITING_STATE',
'ACCOUNT_SUBMENU_STATE',
'ADMIN_SUBMENU_STATE',
'PATIENT_SUBMENU_STATE',
'DOCTOR_SUBMENU_STATE',
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
        self.account_service = None
        self.admin_service = None
        self.doctor_service = None
        self.patient_service = None
    
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
    
    # Polymorphism allows me to repeat the same code for different objects that do different things.

    def account_submenu(self) -> None:
        
        if self.account_service == None:
            self.account_service = AccountService()
        
        if self.account_service.get_state() == account_service_state.CLOSING_STATE:
            print('Are you sure you want to close the application? (Y/N)')
            while True:
                try:
                    user_input = input('>>>').upper()
                    if not self.validate_input(user_input, char_input = True, valid_input = 'YN'):
                        raise MenuSelectionInvalidException("Please enter a valid menu option.")
                    if user_input == 'Y':
                        self.current_state = menu_state.CLOSING_STATE
                    else:
                        self.current_state = menu_state.INITIAL_STATE
                        self.account_service.set_state(account_service_state.INITIAL_STATE)

                    return
                except MenuSelectionInvalidException as msg:
                    print(msg.message)
        
        if self.account_service.get_state() == account_service_state.LOADED_USER_STATE:
            account_role = self.account_service.get_account_role()
            match account_role:
                case 'Admin':
                    self.current_state = menu_state.ADMIN_SUBMENU_STATE
                case 'Patient':
                    self.current_state = menu_state.PATIENT_SUBMENU_STATE
                case 'Doctor':
                    self.current_state = menu_state.DOCTOR_SUBMENU_STATE

            return

        if self.account_service.run(): #run should return True when everything goes well.
            self.reset_state()

    def admin_submenu(self) -> None:
        if self.admin_service == None:
            self.admin_service = AdminService(self.account_service.current_account)

        if self.admin_service.get_state() == admin_service_state.CLOSING_STATE:
            print('Are you sure you want to sign out? (Y/N)')
            while True:
                try:
                    user_input = input('>>>').upper()
                    if not self.validate_input(user_input, char_input = True, valid_input = 'YN'):
                        raise MenuSelectionInvalidException("Please enter a valid menu option.")
                    if user_input == 'Y':
                        self.current_state = menu_state.INITIAL_STATE
                        self.account_service.current_account = None
                        self.account_service.set_state(account_service_state.INITIAL_STATE)
                        self.admin_service = None
                    else:
                        self.current_state = menu_state.INITIAL_STATE
                        self.admin_service.set_state(admin_service_state.INITIAL_STATE)

                    return
                except MenuSelectionInvalidException as msg:
                    print(msg.message)

        if self.admin_service.run():
            self.reset_state()
    
    def patient_submenu(self) -> None:
        if self.patient_service == None:
            self.patient_service = PatientService(self.account_service.current_account)

        if self.patient_service.get_state() == patient_service_state.CLOSING_STATE:
            print('Are you sure you want to sign out? (Y/N)')
            while True:
                try:
                    user_input = input('>>>').upper()
                    if not self.validate_input(user_input, char_input = True, valid_input = 'YN'):
                        raise MenuSelectionInvalidException("Please enter a valid menu option.")
                    if user_input == 'Y':
                        self.current_state = menu_state.INITIAL_STATE
                        self.account_service.current_account = None
                        self.account_service.set_state(account_service_state.INITIAL_STATE)
                        self.patient_service = None
                    else:
                        self.current_state = menu_state.INITIAL_STATE
                        self.patient_service.set_state(patient_service_state.INITIAL_STATE)

                    return
                except MenuSelectionInvalidException as msg:
                    print(msg.message)

        if self.patient_service.run():
            self.reset_state()
    
    def doctor_submenu(self) -> None:
        if self.doctor_service == None:
            self.doctor_service = DoctorService(self.account_service.current_account)

        if self.doctor_service.get_state() == doctor_service_state.CLOSING_STATE:
            print('Are you sure you want to sign out? (Y/N)')
            while True:
                try:
                    user_input = input('>>>').upper()
                    if not self.validate_input(user_input, char_input = True, valid_input = 'YN'):
                        raise MenuSelectionInvalidException("Please enter a valid menu option.")
                    if user_input == 'Y':
                        self.current_state = menu_state.INITIAL_STATE
                        self.account_service.current_account = None
                        self.account_service.set_state(account_service_state.INITIAL_STATE)
                        self.doctor_service = None
                    else:
                        self.current_state = menu_state.INITIAL_STATE
                        self.doctor_service.set_state(patient_service_state.INITIAL_STATE)

                    return
                except MenuSelectionInvalidException as msg:
                    print(msg.message)

        if self.doctor_service.run():
            self.reset_state()

    def close_connections(self) -> None:
        if self.account_service != None:
            self.account_service.close_connections()
        if self.admin_service != None:
            self.admin_service.close_connections()
        if self.doctor_service != None:
            self.doctor_service.close_connections()
        if self.patient_service != None:
            self.patient_service.close_connections()

    def display(self) -> None:
        self.current_state = menu_state.ACCOUNT_SUBMENU_STATE
        if self.account_service == None:
            print('\nWelcome to RXBuddy!')
            print('Please login or register...')
            return
        
    def run(self) -> None:
        match self.current_state:
            case menu_state.INITIAL_STATE:
                self.display()
            case menu_state.ACCOUNT_SUBMENU_STATE:
                self.account_submenu()
            case menu_state.ADMIN_SUBMENU_STATE:
                self.admin_submenu()
            case menu_state.PATIENT_SUBMENU_STATE:
                self.patient_submenu()
            case menu_state.DOCTOR_SUBMENU_STATE:
                self.doctor_submenu()
            
