from custom_exceptions.doctor_menu_selection_invalid import DoctorMenuSelectionInvalid

from interface.doctor_service_interface import DoctorServiceInterface
from interface.input_validation_interface import InputValidation

from implementation.data_access_classes.account_dao import AccountDAO
from implementation.data_access_classes.medication_dao import MedicationDAO
from implementation.data_access_classes.prescription_dao import PrescriptionDAO

from implementation.data_model_classes.account import Account
from implementation.data_model_classes.medication import Medication
from implementation.data_model_classes.prescription import Prescription

from enum import Enum

doctor_service_state = Enum('DOCTOR_STATE', [
    'INITIAL_STATE',
    'CREATE_PRESCRIPTION_STATE',
    'MODIFY_PRESCRIPTIONS_STATE',
    'MODFIY_MEDICATIONS_STATE',
    'CLOSING_STATE'
])

class DoctorService(InputValidation, DoctorServiceInterface):
    def __init__(self, current_account: Account):
        self.current_state = doctor_service_state.INITIAL_STATE
        self.account_dao: AccountDAO = AccountDAO()
        self.medication_dao: MedicationDAO = MedicationDAO()
        self.prescriptions_dao: PrescriptionDAO = PrescriptionDAO()

        self.accounts: list[Account] = None 
        self.medications: list[Medication] = None
        self.prescriptions: list[Prescription] = None

        self.current_account = current_account

     
    def set_state(self, state_value: int) -> None:
        self.current_state = state_value
    
    def get_state(self) -> int:
        return self.current_state
    
    def get_medication_from_list(self, med_id: int,  med_list: list[Medication]) -> Medication:
        target_med = list(filter(lambda item: item.medicationID == med_id, med_list))
        return target_med[0]
    
    def get_account_from_list(self, accountID: int, account_list: list[Account]) -> Account:
        target_account = list(filter(lambda item: item.accountID == accountID, account_list))
        return target_account[0]
    
    def display_prescriptions(self) -> None:
        print('\nThe following are all of your patients that received a prescription in the database: ')
        # valid_IDs = set()
        result_str = ''
        for prescription in self.prescriptions:
            result_str += f'{prescription.prescriptionID}. Username: {prescription.prescribedToUsername} - Name: {prescription.prescribedToFirstName} {prescription.prescribedToLastName} - Medication Name: {prescription.medicationName}\n'
            # valid_IDs.add(account.accountID)
        print(result_str)
        submenu_option = ''
        while True:
            try: 
                print('Choose an option: ')
                print('A. Modify prescriptions - NOT IMPLEMENTED')
                print('B. Cancel')
                submenu_option = input('>>>').upper()
                if not self.validate_input(submenu_option, char_input=True, valid_input='B'):
                    raise DoctorMenuSelectionInvalid('Please select a valid submenu option.')
                break
            except DoctorMenuSelectionInvalid as err:
                print(err.message)
        
        if submenu_option == 'B':
            self.current_state = doctor_service_state.INITIAL_STATE
            return True

    
    def display_medications(self) -> None:
        print('\nThe following are all the medications in the database: ')
        # valid_IDs = set()
        result_str = ''
        for medication in self.medications:
            result_str += f'{medication.medicationID}. Name: {medication.medicationName} - Cost: ${medication.medicationCost}\n'
            # valid_IDs.add(account.accountID)
        print(result_str)
        submenu_option = ''
        while True:
            try: 
                print('Choose an option: ')
                print('A. Modify medications - NOT IMPLEMENTED')
                print('B. Cancel')
                submenu_option = input('>>>').upper()
                if not self.validate_input(submenu_option, char_input=True, valid_input='B'):
                    raise DoctorMenuSelectionInvalid('Please select a valid submenu option.')
                break
            except DoctorMenuSelectionInvalid as err:
                print(err.message)
        
        if submenu_option == 'B':
            self.current_state = doctor_service_state.INITIAL_STATE
            return True
    
    def display_patients(self) -> None:
        print('\nThe following are all the patients in the database: ')
        valid_IDs = set()
        result_str = ''
        for account in self.accounts:
            result_str += f'{account.accountID}. {account.accountUsername} - Name: {account.firstName} {account.lastName};\n'
            valid_IDs.add(account.accountID)
        print(result_str)
        submenu_option = ''
        while True:
            try: 
                print('Choose an option: ')
                print('A. Prescribe medication(s)')
                print('B. Cancel')
                submenu_option = input('>>>').upper()
                if not self.validate_input(submenu_option, char_input=True, valid_input='AB'):
                    raise DoctorMenuSelectionInvalid('Please select a valid submenu option.')
                break
            except DoctorMenuSelectionInvalid as err:
                print(err.message)
        
        if submenu_option == 'B':
            self.current_state = doctor_service_state.INITIAL_STATE
            return True
        patient_account: Account = None
        while True:
            try: 
                print('Select a patient (enter their ID): ')
                user_input = input('>>>')
                if not self.validate_input(user_input, integer_input=True):
                    raise DoctorMenuSelectionInvalid('Please select a valid account ID from the list.')
                if int(user_input) not in valid_IDs:
                    raise DoctorMenuSelectionInvalid('Please select a valid account ID from the list. ')
                patient_account = self.get_account_from_list(int(user_input), self.accounts)
                break
            except DoctorMenuSelectionInvalid as err: 
                print(err.message)
        
        while True:
            try: 
                print('The following are prescribable medications: ')
                valid_medIDs = set()
                result_medStr = ''
                for medication in self.medications:
                    result_medStr += f'{medication.medicationID}. Name: {medication.medicationName}\n'
                    valid_medIDs.add(medication.medicationID)

                print(result_medStr)
                print('\nSelect medications to prescribe (enter their IDs separated by spaces): ')
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
                    raise DoctorMenuSelectionInvalid('One or more inputs were invalid, please make sure to input valid IDs.')

                self.prescriptions_dao.create_prescriptions_from_list(self.current_account, patient_account, medication_list)
                self.prescriptions = self.prescriptions_dao.get_all_prescriptions()
                break
            except DoctorMenuSelectionInvalid as err: 
                print(err.message)

        print(f'Successfully prescribed the specified medications to {patient_account.accountUsername}!')
        self.current_state = doctor_service_state.INITIAL_STATE
        return True

    def process_input(self, input):
        match (input):
            case 'A':
                self.current_state = doctor_service_state.CREATE_PRESCRIPTION_STATE
            case 'B':
                self.current_state = doctor_service_state.MODIFY_PRESCRIPTIONS_STATE
            case 'C':
                self.current_state = doctor_service_state.MODFIY_MEDICATIONS_STATE
            case 'D':
                self.current_state = doctor_service_state.CLOSING_STATE

    def close_connections(self) -> bool:
        """
            This method closes connections if they exist.
        """
        if self.account_dao.current_connection != None:
            self.account_dao.close_connection()
        if self.medication_dao.current_connection != None:
            self.medication_dao.close_connection()
        if self.prescriptions_dao.current_connection != None:
            self.prescriptions_dao.close_connection()
        
    def display(self) -> None:
        self.accounts = self.account_dao.get_all_patients()
        self.medications = self.medication_dao.get_all_medications()
        self.prescriptions = self.prescriptions_dao.get_prescriptions_by_doctorID(self.current_account.accountID)
        print('\nWhat would you like to do? ')
        print('A. Prescribe a medication')
        print('B. View my patients')
        print('C. View all medications')
        print('D. Sign out')
        while self.current_state == doctor_service_state.INITIAL_STATE:
            try:
                user_input = input('>>>').upper()
                if not self.validate_input(user_input, char_input = True, valid_input = 'ABCD'):
                    raise DoctorMenuSelectionInvalid("Please choose a valid submenu option.")
                self.process_input(user_input)
            except DoctorMenuSelectionInvalid as err:
                print(err.message) #note logging is handled when exception is created.

        return True

    
    def run(self) -> None:
        match self.current_state:
            case doctor_service_state.INITIAL_STATE:
                return self.display()
            case doctor_service_state.CREATE_PRESCRIPTION_STATE:
                return self.display_patients()
            case doctor_service_state.MODIFY_PRESCRIPTIONS_STATE:
                return self.display_prescriptions()
            case doctor_service_state.MODFIY_MEDICATIONS_STATE:
                return self.display_medications()
            case doctor_service_state.CLOSING_STATE:
                return True