from custom_exceptions.admin_menu_selection_invalid import AdminMenuSelectionInvalid
from custom_exceptions.medication_invalid import MedicationInvalid

from interface.admin_service_interface import AdminServiceInterface
from interface.input_validation_interface import InputValidation

from implementation.data_access_classes.account_dao import AccountDAO
from implementation.data_access_classes.medication_dao import MedicationDAO
from implementation.data_access_classes.orders_dao import OrdersDAO

from implementation.data_model_classes.account import Account
from implementation.data_model_classes.medication import Medication
from implementation.data_model_classes.shop_order import Shop_Order

from enum import Enum

admin_service_state = Enum('ADMIN_STATE', [
    'INITIAL_STATE',
    'ACCOUNTS_STATE',
    'MEDICATIONS_STATE',
    'ORDERS_STATE',
    'CLOSING_STATE'
])

class AdminService(InputValidation, AdminServiceInterface):
    def __init__(self, current_account):
        self.current_state = admin_service_state.INITIAL_STATE
        self.account_dao: AccountDAO = AccountDAO()
        self.medication_dao: MedicationDAO = MedicationDAO()
        self.orders_dao: OrdersDAO = OrdersDAO()

        self.accounts: list[Account] = None
        self.medications: list[Medication] = None
        self.shop_orders: list[Shop_Order] = None

        self.current_account = current_account

    def set_state(self, state_value: int) -> None:
        self.current_state = state_value

    def get_state(self) -> int:
        return self.current_state
    
    def display_accounts(self) -> bool:
        print('\nThe following are all the accounts in the database (excluding you): ')
        valid_IDs = set()
        result_str = ''
        for account in self.accounts:
            if account.accountID == self.current_account.accountID:
                continue
            result_str += f'{account.accountID}. {account.accountUsername} - Name: {account.firstName} {account.lastName}; Balance: {account.balance}; Role: {account.roleName}\n'
            valid_IDs.add(account.accountID)
        print(result_str)
        submenu_option = ''
        while True:
            try: 
                print('Choose an option: ')
                print('A. Change role')
                print('B. Delete account')
                print('C. Exit')
                submenu_option = input('>>>').upper()
                if not self.validate_input(submenu_option, char_input=True, valid_input='ABC'):
                    raise AdminMenuSelectionInvalid('Please select a valid submenu option.')
                break
            except AdminMenuSelectionInvalid as err:
                print(err.message)
        
        if submenu_option == 'C':
            self.current_state = admin_service_state.INITIAL_STATE
            return True
        
        while True:
            try: 
                print('Select an account to modify (enter its ID): ')
                user_input = input('>>>')
                if not self.validate_input(user_input, integer_input=True):
                    raise AdminMenuSelectionInvalid('Please select a valid account ID from the list.')
                if int(user_input) not in valid_IDs:
                    raise AdminMenuSelectionInvalid('Please select a valid account ID from the list. ')
                match submenu_option:
                    case 'A':
                        self.apply_role(int(user_input))
                        self.accounts = self.account_dao.get_all_accounts()
                    case 'B':
                        self.account_dao.delete_account_by_id(int(user_input))
                        self.accounts = self.account_dao.get_all_accounts()
                break
            except AdminMenuSelectionInvalid as err: 
                print(err.message)

        self.current_state = admin_service_state.INITIAL_STATE
        return True
    
    def display_orders(self) -> None:
        self.shop_orders = self.orders_dao.get_all_orders()
        print('\nThe following are all the orders in the database: ')
        # valid_IDs = set()
        result_str = ''
        for order in self.shop_orders:
            result_str += f'{order.orderID}. Username: {order.username} - Name: {order.firstName} {order.lastName} - Medication: {order.medicationName} - Total Amount: ${order.medicationCost}\n'
            # valid_IDs.add(account.accountID)
        print(result_str)
        submenu_option = ''
        while True:
            try: 
                print('Choose an option: ')
                print('A. Modify orders - NOT IMPLEMENTED')
                print('B. Cancel')
                submenu_option = input('>>>').upper()
                if not self.validate_input(submenu_option, char_input=True, valid_input='B'):
                    raise AdminMenuSelectionInvalid('Please select a valid submenu option.')
                break
            except AdminMenuSelectionInvalid as err:
                print(err.message)
        
        if submenu_option == 'B':
            self.current_state = admin_service_state.INITIAL_STATE
            return True

    def display_remove_medication(self, valid_ids:set[int]) -> None:
        medid_input = ''
        while True:
            try:
                print('Please enter the medication\'s id: ')
                medid_input = input('>>>')
                if not self.validate_input(medid_input, integer_input=True):
                    raise MedicationInvalid('Medication id must be numerical.')
                
                if int(medid_input) not in valid_ids:
                    raise MedicationInvalid('Medication id must be in the list above.')

                break
            except MedicationInvalid as err:
                print(err.message)

        self.medication_dao.delete_medication(int(medid_input))
        print('Medication deleted successfully.')

    def display_add_medication(self) -> None:
        medname_input = ''
        medcost_input = ''
        while True:
            try:
                print('Please enter the medication\'s name: ')
                medname_input = input('>>>')
                if not self.validate_input(medname_input, string_input=True):
                    raise MedicationInvalid('Medication name must have more than 2 characters and be alphabetical.')
                
                print('Please enter the medication\'s cost: ')
                medcost_input = input('>>>')
                if not self.validate_input(medcost_input, integer_input=True):
                    raise MedicationInvalid('Please enter a valid dollar amount.')

                break
            except MedicationInvalid as err:
                print(err.message)

        self.medication_dao.create_medication(Medication(0, medname_input, float(medcost_input)))
        print('Medication added successfully.')

    def display_medications(self) -> None:
        self.medications = self.medication_dao.get_all_medications()
        print('\nThe following are all the medications in the database: ')
        valid_IDs = set()
        result_str = ''
        for medication in self.medications:
            result_str += f'{medication.medicationID}. Name: {medication.medicationName} - Cost: ${medication.medicationCost}\n'
            valid_IDs.add(medication.medicationID)
        print(result_str)
        submenu_option = ''
        while True:
            try: 
                print('Choose an option: ')
                print('A. Modify medications')
                print('B. Cancel')
                submenu_option = input('>>>').upper()
                if not self.validate_input(submenu_option, char_input=True, valid_input='AB'):
                    raise AdminMenuSelectionInvalid('Please select a valid submenu option.')
                break
            except AdminMenuSelectionInvalid as err:
                print(err.message)
        
        if submenu_option == 'B':
            self.current_state = admin_service_state.INITIAL_STATE
            return True
        
        while True:
            try: 
                print('Choose an option: ')
                print('A. Add Medication')
                print('B. Delete Medication')
                print('C. Cancel')
                submenu_option = input('>>>').upper()
                if not self.validate_input(submenu_option, char_input=True, valid_input='ABC'):
                    raise AdminMenuSelectionInvalid('Please select a valid submenu option.')
                break
            except AdminMenuSelectionInvalid as err:
                print(err.message)

        if submenu_option == 'C':
            self.current_state = admin_service_state.INITIAL_STATE
            return True
        elif submenu_option == 'A':
            self.display_add_medication()
        elif submenu_option == 'B':
            self.display_remove_medication(valid_IDs)

        self.current_state = admin_service_state.INITIAL_STATE
        return True



    def apply_role(self, accountID) -> None:
        submenu_option = ''
        while True:
            try:
                print('Choose a role to apply: ')
                print('A. Admin')
                print('B. Patient')
                print('C. Doctor')
                print('D. Cancel')
                submenu_option = input('>>>').upper()
                if not self.validate_input(submenu_option, char_input=True, valid_input='ABCD'):
                    raise AdminMenuSelectionInvalid('Please choose a valid submenu option.')
                break
            except AdminMenuSelectionInvalid as err:
                print(err.message)

        if submenu_option == 'D':
            self.current_state = admin_service_state.INITIAL_STATE
            return 
        
        old_account = self.account_dao.get_account_by_id(accountID)
        roleUse = ''
        if submenu_option == 'A':
            roleUse = 'Admin'
        elif submenu_option == 'B':
            roleUse = 'Patient'
        else:
            roleUse = 'Doctor'
        
        new_account = Account(old_account.accountID, old_account.accountUsername, old_account.accountPassword, old_account.firstName, old_account.lastName, old_account.balance, roleUse)
        self.account_dao.update_account(new_account)
        print('Role updated successfully.')

    def process_input(self, input):
        match (input):
            case 'A':
                self.current_state = admin_service_state.MEDICATIONS_STATE
            case 'B':
                self.current_state = admin_service_state.ACCOUNTS_STATE
            case 'C':
                self.current_state = admin_service_state.ORDERS_STATE
            case 'D':
                self.current_state = admin_service_state.CLOSING_STATE

    def close_connections(self) -> bool:
        """
            This method closes connections if they exist.
        """
        if self.account_dao.current_connection != None:
            self.account_dao.close_connection()
        if self.medication_dao.current_connection != None:
            self.medication_dao.close_connection()
        if self.orders_dao.current_connection != None:
            self.orders_dao.close_connection()
        
    def display(self) -> None:
        self.accounts = self.account_dao.get_all_accounts()
        print('\nWhat would you like to do? ')
        print('A. View all medications.')
        print('B. Modify or View accounts.')
        print('C. View all orders.')
        print('D. Sign out.')
        while self.current_state == admin_service_state.INITIAL_STATE:
            try:
                user_input = input('>>>').upper()
                if not self.validate_input(user_input, char_input = True, valid_input = 'ABCD'):
                    raise AdminMenuSelectionInvalid("Please choose a valid submenu option.")
                self.process_input(user_input)
            except AdminMenuSelectionInvalid as err:
                print(err.message) #note logging is handled when exception is created.

        return True
    
    def run(self) -> None:
        match self.current_state:
            case admin_service_state.INITIAL_STATE:
                return self.display()
            case admin_service_state.ACCOUNTS_STATE:
                return self.display_accounts()
            case admin_service_state.MEDICATIONS_STATE:
                return self.display_medications()
            case admin_service_state.ORDERS_STATE:
                return self.display_orders()
            case admin_service_state.CLOSING_STATE:
                return True