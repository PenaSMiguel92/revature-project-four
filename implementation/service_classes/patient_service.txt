from interface.patient_service_interface import PatientServiceInterface
from interface.input_validation_interface import InputValidation

from implementation.data_access_classes.prescription_dao import PrescriptionDAO
from implementation.data_access_classes.orders_dao import OrdersDAO
from implementation.data_access_classes.medication_dao import MedicationDAO

from implementation.data_model_classes.account import Account
from implementation.data_model_classes.medication import Medication
from implementation.data_model_classes.prescription import Prescription
from implementation.data_model_classes.shop_order import Shop_Order

from custom_exceptions.patient_menu_selection_invalid import PatientMenuSelectionInvalid
from custom_exceptions.order_invalid import OrderInvalid

from enum import Enum

patient_service_state = Enum('PATIENT_STATE', [
    'INITIAL_STATE',
    'PRESCRIPTIONS_STATE',
    'ORDERS_STATE',
    'CLOSING_STATE'
])

class PatientService(InputValidation, PatientServiceInterface):
    def __init__(self, current_account: Account):
        self.current_state = patient_service_state.INITIAL_STATE
        self.prescriptions_dao: PrescriptionDAO = PrescriptionDAO()
        self.orders_dao: OrdersDAO = OrdersDAO()
        self.medication_dao: MedicationDAO = MedicationDAO()

        self.prescriptions: list[Prescription] = self.prescriptions_dao.get_prescriptions_by_patientID(current_account.accountID)
        self.orders: list[Shop_Order] = self.orders_dao.get_orders_by_username(current_account.accountUsername)
        self.medications: list[Medication] = self.medication_dao.get_all_medications()

        self.current_account = current_account
     
    def set_state(self, state_value: int) -> None:
        self.current_state = state_value
    
    def get_state(self) -> int:
        return self.current_state
    
    def display_remove_orders(self, valid_ids:set[int]) -> None:
        orderid_input = ''
        while True:
            try:
                print('Please enter the order\'s id: ')
                orderid_input = input('>>>')
                if not self.validate_input(orderid_input, integer_input=True):
                    raise OrderInvalid('Order id must be numerical.')
                
                if int(orderid_input) not in valid_ids:
                    raise OrderInvalid('Order id must be in the list above.')

                break
            except OrderInvalid as err:
                print(err.message)

        self.orders_dao.delete_order_by_id(int(orderid_input))
        print('Order deleted successfully.')

    def display_orders(self) -> bool:
        self.orders = self.orders_dao.get_orders_by_username(self.current_account.accountUsername)
        if len(self.orders) < 1:
            print('\nYou do not have any orders at this time.')
            self.current_state = patient_service_state.INITIAL_STATE
            return True
        
        print('\nThese are all your orders: ')
        result_str = ''
        valid_orderIDs = set()
        for order in self.orders:
            result_str += f'Order ID: {order.orderID} - Product: {order.medicationName} - Total: ${order.medicationCost} \n'
            valid_orderIDs.add(order.orderID)

        print(result_str)
        submenu_option = ''
        while True:
            try: 
                print('Choose an option: ')
                print('A. Cancel an order')
                print('B. Exit')
                submenu_option = input('>>>').upper()
                if not self.validate_input(submenu_option, char_input=True, valid_input='AB'):
                    raise PatientMenuSelectionInvalid('Please select a valid submenu option.')
                break
            except PatientMenuSelectionInvalid as err:
                print(err.message)
        
        if submenu_option == 'B':
            self.current_state = patient_service_state.INITIAL_STATE
            return True
        elif submenu_option == 'A':
            self.display_remove_orders(valid_orderIDs)

        self.current_state = patient_service_state.INITIAL_STATE
        return True

    def get_medication_from_list(self, med_id: int,  med_list: list[Medication]) -> Medication:
        target_med = list(filter(lambda item: item.medicationID == med_id, med_list))
        return target_med[0]

    def display_prescriptions(self) -> bool:
        self.prescriptions = self.prescriptions_dao.get_prescriptions_by_patientID(self.current_account.accountID)
        if len(self.prescriptions) < 1:
            print('\nYou do not have any prescriptions at this time.')
            self.current_state = patient_service_state.INITIAL_STATE
            return True
        
        print('\nThese are the medications prescribed to you: ')
        result_str = ''
        valid_medIDs = set()
        for prescription in self.prescriptions:
            result_str += f'ID: {prescription.prescriptionID} - {prescription.medicationName}\n'
            valid_medIDs.add(prescription.prescriptionID)
        
        print(result_str)
        while True:
            try: 
                print('\nWhich would you like to purchase? (separate IDs by spaces)')
                user_input = input('>>>').split()
                medication_list: list[Medication] = []
                one_or_more_invalid = False
                for input_value in user_input:
                    if not self.validate_input(input_value, integer_input=True):
                        one_or_more_invalid = True
                        continue
                    if int(input_value) not in valid_medIDs:
                        one_or_more_invalid = True
                        continue
                    medication_list.append(self.get_medication_from_list(int(input_value), self.medications))
                
                if one_or_more_invalid:
                    raise PatientMenuSelectionInvalid('One or more inputs were invalid, please make sure to input valid IDs.')

                self.current_account = self.orders_dao.create_orders_from_list(self.current_account, medication_list)
                if self.current_account:
                    break
            except PatientMenuSelectionInvalid as err:
                print(err.message)

        print('Orders successfully submitted.')
        print(f'\nYour balanace is now: ${self.current_account.balance}')
        self.current_state = patient_service_state.INITIAL_STATE
        return True
    
    def process_input(self, input: str) -> None:
        match (input):
            case 'A':
                self.current_state = patient_service_state.PRESCRIPTIONS_STATE
            case 'B':
                self.current_state = patient_service_state.ORDERS_STATE
            case 'C':
                self.current_state = patient_service_state.CLOSING_STATE

    def close_connections(self) -> bool:
        """
            This method closes connections if they exist.
        """
        if self.orders_dao.current_connection != None:
            self.orders_dao.close_connection()
        if self.medication_dao.current_connection != None:
            self.medication_dao.close_connection()
        if self.prescriptions_dao.current_connection != None:
            self.prescriptions_dao.close_connection()
        

    def display(self) -> bool:
        
        
        print('\nWould you like to make or modify an order? ')
        print('A. Make an order.')
        print('B. Modify an order.')
        print('C. Sign out.')
        while self.current_state == patient_service_state.INITIAL_STATE:
            try:
                user_input = input('>>>').upper()
                if not self.validate_input(user_input, char_input = True, valid_input = 'ABC'):
                    raise PatientMenuSelectionInvalid("Please choose a valid menu option.")
                self.process_input(user_input)
            except PatientMenuSelectionInvalid as err:
                print(err.message) #note logging is handled when exception is created.

        return True
    
    def run(self) -> bool:
        match self.current_state:
            case patient_service_state.INITIAL_STATE:
                return self.display()
            case patient_service_state.PRESCRIPTIONS_STATE:
                return self.display_prescriptions()
            case patient_service_state.ORDERS_STATE:
                return self.display_orders()
            case patient_service_state.CLOSING_STATE:
                return True