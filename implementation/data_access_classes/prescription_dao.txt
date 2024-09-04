from interface.data_access_object_interface import DataAccessObjectInterface
from implementation.data_model_classes.account import Account
from implementation.data_model_classes.medication import Medication
from implementation.data_model_classes.prescription import Prescription
import logging

import mysql.connector
from mysql.connector.cursor import MySQLCursor

class PrescriptionDAO(DataAccessObjectInterface):
    def __init__(self):
        logging.basicConfig(filename="logs/rxbuddy_database.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')

    def get_all_prescriptions(self) -> list[Prescription]:
        """
            This method will cache all prescriptions from the prescriptions table to a list.
            
            This method should only be accessible by an admin, and run only once per session.

            This method will return a list of Prescription ORM objects if transaction was successful, raise an exception otherwise.
        """
        cursor: MySQLCursor = super().get_cursor()
        query_columns = 'SELECT p.prescriptionID, doctor.accountUsername, patient.accountUsername, patient.firstName, patient.lastName, m.medicationName '
        query_joining_firstPart = 'FROM prescriptions AS p JOIN accounts AS doctor ON p.prescribedBy=doctor.accountID '
        query_joining_secondPart = 'JOIN accounts AS patient ON p.prescribedTo=patient.accountID JOIN medications AS m ON p.medicationID=m.medicationID;'
        cursor.execute(query_columns + query_joining_firstPart + query_joining_secondPart)
        prescriptions: list[Prescription] = [Prescription(int(row[0]), row[1], row[2], row[3], row[4], row[5]) for _, row in enumerate(cursor)]

        logging.info('All prescriptions were retrieved successfully.')
        return prescriptions

    def get_prescriptions_by_patientID(self, patientID: int) -> list[Prescription]:
        """
            This method will return prescriptions associated with provided accountID.

            The patient must use this method to get all of their prescriptions. 

            This method will return a list of Prescription ORM objects if transaction was successful, raise an exception otherwise.
        """
        cursor: MySQLCursor = super().get_cursor()
        query_columns = 'SELECT p.prescriptionID, doctor.accountUsername, patient.accountUsername, patient.firstName, patient.lastName, m.medicationName '
        query_joining_firstPart = 'FROM prescriptions AS p JOIN accounts AS doctor ON p.prescribedBy=doctor.accountID '
        query_joining_secondPart = 'JOIN accounts AS patient ON p.prescribedTo=patient.accountID JOIN medications AS m ON p.medicationID=m.medicationID '
        query_condition = f' WHERE patient.accountID={patientID};'
        cursor.execute(query_columns + query_joining_firstPart + query_joining_secondPart + query_condition)
        prescriptions: list[Prescription] = [Prescription(int(row[0]), row[1], row[2], row[3], row[4], row[5]) for _, row in enumerate(cursor)]

        logging.info(f'All prescriptions for patient ID: {patientID} were retrieved successfully.')
        return prescriptions
    
    def get_prescriptions_by_doctorID(self, doctorID: int) -> list[Prescription]:
        """
            This method will return prescriptions associated with provided accountID.

            A doctor must use this method to get all of their prescribed prescriptions. 

            This method will return a list of Prescription ORM objects if transaction was successful, raise an exception otherwise.
        """
        cursor: MySQLCursor = super().get_cursor()
        query_columns = 'SELECT p.prescriptionID, doctor.accountUsername, patient.accountUsername, patient.firstName, patient.lastName, m.medicationName '
        query_joining_firstPart = 'FROM prescriptions AS p JOIN accounts AS doctor ON p.prescribedBy=doctor.accountID '
        query_joining_secondPart = 'JOIN accounts AS patient ON p.prescribedTo=patient.accountID JOIN medications AS m ON p.medicationID=m.medicationID '
        query_condition = f' WHERE doctor.accountID={doctorID};'
        cursor.execute(query_columns + query_joining_firstPart + query_joining_secondPart + query_condition)
        prescriptions: list[Prescription] = [Prescription(int(row[0]), row[1], row[2], row[3], row[4], row[5]) for _, row in enumerate(cursor)]

        logging.info(f'All prescriptions by doctor ID: {doctorID} were retrieved successfully.')
        return prescriptions
    
    def create_prescription(self, doctor: Account, patient: Account, medication: Medication) -> bool:
        """
            This method will craate a prescription and insert it into the prescriptions table for saving.

            This method takes in a doctor account, a patient account, and medication object and saves accordingly for joining.

            This method will return a boolean True value if transaction was successful, raise an exception otherwise.
        """
        cursor: MySQLCursor = super().get_cursor()
        query_start = 'INSERT INTO prescriptions (prescriptionID, prescribedBy, prescribedTo, medicationID) VALUES '
        query_end = f'(DEFAULT, {doctor.accountID}, {patient.accountID}, {medication.medicationID});'
        cursor.execute(query_start + query_end)

        super().commit_changes()
        logging.info(f'Created prescription by {doctor.lastName} to {patient.lastName} the medication {medication.medicationName} and saved to the database.')
        return True
    
    def create_prescriptions_from_list(self, doctor: Account, patient: Account, med_list: list[Medication]) -> bool:
        cursor: MySQLCursor = super().get_cursor()
        query_str = 'INSERT INTO prescriptions (prescriptionID, prescribedBy, prescribedTo, medicationID) VALUES '
        for index, med in enumerate(med_list):
            if index == len(med_list) - 1:
                query_str += f'(DEFAULT, {doctor.accountID}, {patient.accountID}, {med.medicationID});'
                continue
            query_str += f'(DEFAULT, {doctor.accountID}, {patient.accountID}, {med.medicationID}),'
        cursor.execute(query_str)

        super().commit_changes()
        logging.info(f'Created prescriptions by {doctor.lastName} to {patient.lastName} a list of medications and saved to the database.')
        return True
    
    def update_prescription(self, prescription: Prescription, medication: Medication) -> bool:
        """
            This method takes in a prescription object and a medication object, and updates the medicationID accordingly.

            A doctor can change a prescription if an error occured. 

            This method will return a boolean True value if transaction was successful, raise an exception otherwise. 
        """
        cursor: MySQLCursor = super().get_cursor()
        query_start = f'UPDATE prescriptions SET medicationID={medication.medicationID} '
        query_end = f'WHERE prescriptionID={prescription.prescriptionID};'
        cursor.execute(query_start, query_end)
        super().commit_changes()
        logging.info(f'Prescription of ID: {prescription.prescriptionID} had its medicationID updated to {medication.medicationID} in the database.')
        return True

    def delete_prescription_by_id(self, prescription_id: int) -> bool:
        """
            This method will delete an prescription with the specified id.

            This method can be used to cancel an prescription, the patient will no longer be able to view or order it.

            This method will return a boolean True value if transaction was successful, raise an exception otherwise.
        """
        try:
            cursor: MySQLCursor = super().get_cursor()
            query = f'DELETE FROM prescriptions WHERE prescriptionID={prescription_id};'
            cursor.execute(query)

        except mysql.connector.Error as Err:
            print("Please choose a valid ID to delete.")
            logging.error(Err.msg)
            return False
        
        super().commit_changes()
        logging.info(f'Deleted prescription with ID: {prescription_id} from prescriptions table in database.')
        return True   

        