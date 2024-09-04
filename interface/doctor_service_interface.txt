from abc import abstractmethod
from interface.menu_baseclass import MenuBaseClass

class DoctorServiceInterface(MenuBaseClass):
    @abstractmethod
    def set_state(self, state_value: int) -> None:
        ...

    @abstractmethod
    def get_state(self) -> int:
        ...
    
    @abstractmethod
    def display_prescriptions(self) -> None:
        """
            This method displays all prescriptions by this doctor, and provides an interface for modifying prescriptions.
        """
        ...

    @abstractmethod
    def display_medications(self) -> None:
        """
            This method displays all medications and provides an interface for choosing a medication for prescribing.
        """
        ...
    
    @abstractmethod
    def display_patients(self) -> None:
        """
            This method displays all accounts that are patients, and provides an interface for prescribing.
        """
        ...

    @abstractmethod
    def process_input(self) -> None:
        """
            Method for processing user input.
        """
        ...

    @abstractmethod
    def close_connections(self) -> bool:
        """
            This method closes connections if they exist.
        """
        ...