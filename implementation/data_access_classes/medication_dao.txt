from interface.data_access_object_interface import DataAccessObjectInterface
from implementation.data_model_classes.medication import Medication
import logging
import mysql.connector
from mysql.connector.cursor import MySQLCursor

class MedicationDAO(DataAccessObjectInterface):
    """
        This class is meant for retrieving medications from the medications table. 
    """
    def __init__(self):
        logging.basicConfig(filename="logs/rxbuddy_database.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')
    
    def get_all_medications(self) -> list[Medication]:
        """
            This method will return all medications from the medications table.
            
            This method should only be accessible by an admin or doctor.

            This method will return a list of medications if transaction was successful, raise an exception otherwise.
        """
        cursor: MySQLCursor = super().get_cursor()
        query = 'SELECT * FROM medications;'
        cursor.execute(query)
        medications: list[Medication] = []
        for _, row in enumerate(cursor):
            medications.append(Medication(int(row[0]), row[1], float(row[2])))

        logging.info('All medications retrieved from database successfully.')
        return medications

    def get_medication_by_name(self, name: str) -> Medication:
        """
            This method will return medication associated with provided name. 

            This method should be accessible from the prescription submenu. 

            This method will return a Medication object if transaction was successful, raise an exception otherwise.
        """
        cursor: MySQLCursor = super().get_cursor()
        query = f'SELECT * FROM medications WHERE medicationName=\'{name}\';'
        cursor.execute(query)
        for _, row in enumerate(cursor):
            medication_result: Medication = Medication(int(row[0]), row[1], float(row[2]))
            break

        logging.info(f'Medication with ID: {medication_result.medicationID} retrieved from database successfully.')
        return medication_result

    def create_medication(self, medication: Medication) -> bool:
        """
            This method will create a new record for the provided Medication object.
        """
        cursor: MySQLCursor = super().get_cursor()
        query_start = f'INSERT INTO medications (medicationID, medicationName, medicationCost) VALUES '
        query_end = f'(DEFAULT, \'{medication.medicationName}\', {medication.medicationCost})'
        cursor.execute(query_start + query_end)
        super().commit_changes()
        logging.info('Medication created and saved to database.')
        return True

    def update_medication(self, medication: Medication) -> bool:
        """
            This method will update an existing medication in the medications table with the provided Medication object's new values.
        """
        cursor: MySQLCursor = super().get_cursor()
        query_start = f'UPDATE medications SET medicationName={medication.medicationName}, medicationCost={medication.medicationCost}'
        query_end = f' WHERE medicationID={medication.medicationID};'
        cursor.execute(query_start + query_end)
        super().commit_changes()
        logging.info(f'Medication with ID: {medication.medicationID} had its attributes updated on the database.')
        return True

    def delete_medication(self, medicationID: int) -> bool:
        """
            This method will delete an medication with the specified medicationID.

            This method will delete orders and prescriptions that refer to this medication.

            This method will return a boolean True value if transaction was successful, raise an exception otherwise.
        """
        try:
            cursor: MySQLCursor = super().get_cursor()
            query_orders = f'DELETE FROM orders WHERE medicationID={medicationID};'
            query_prescriptions = f'DELETE FROM prescriptions WHERE medicationID={medicationID};'
            query_medications = f'DELETE FROM medications WHERE medicationID={medicationID};'

            cursor.execute(query_orders)
            cursor.execute(query_prescriptions)
            cursor.execute(query_medications)

        except mysql.connector.Error as Err:
            logging.error(Err.msg)
            return False
        
        super().commit_changes()
        logging.info(f'Deleted medication with ID: {medicationID} from medications table in database.')
        return True        

    
