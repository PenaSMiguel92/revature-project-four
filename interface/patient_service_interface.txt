from abc import abstractmethod
from interface.menu_baseclass import MenuBaseClass

class PatientServiceInterface(MenuBaseClass):
    @abstractmethod
    def set_state(self, state_value: int) -> None:
        ...

    @abstractmethod
    def get_state(self) -> int:
        ...

    @abstractmethod
    def process_input(self, input: str) -> None:
        """
            Change state based on user input.
        """
        ...
    
    @abstractmethod
    def display_orders(self) -> bool:
        """
            Displays all orders by this patient, and provides an interface for orders.

            Returns a boolean True value when user wants to log off from this submenu.
        """
        ...
    
    @abstractmethod
    def display_prescriptions(self) -> bool:
        """
            Displays all prescribed medications to this patient, and provides an interface for purchasing and creating orders.

            Returns a boolean True value when user wants to log off from this submenu.
        """
        ...

    @abstractmethod
    def close_connections(self) -> bool:
        """
            This method closes connections if they exist.
        """
        ...
    