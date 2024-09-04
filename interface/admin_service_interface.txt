from abc import abstractmethod
from interface.menu_baseclass import MenuBaseClass

class AdminServiceInterface(MenuBaseClass):
    @abstractmethod
    def set_state(self, state_value: int) -> None:
        """
            This method must be used to set the state of this menu.
        """
        ...

    @abstractmethod
    def get_state(self) -> int:
        """
            This method is used to get the state of this menu.
        """
        ...
    
    @abstractmethod
    def display_accounts(self) -> None:
        """
            This method will display all users and their roles.
            For example:
            penamiguel -> Patient
            drhousemd -> Doctor
            ownermiguel -> Admin

            It will also provide an interface for modifying accounts.
        """
        ...
    
    @abstractmethod
    def display_orders(self) -> None:
        """
            This method will display all orders and provide an interface for modifying orders.  
        """
        ...

    @abstractmethod
    def display_medications(self) -> None:
        """
            This method will display all medications and provide an interface for modifying medications.  
        """
        ...

    @abstractmethod
    def apply_role(self) -> None:
        """
            This method will apply a role to a specified user.

            For example, an admin will be able to apply the Doctor role to a user, which grants them the ability to create prescriptions.
        """
        ...

    @abstractmethod
    def process_input(self) -> None:
        ...

    @abstractmethod
    def close_connections(self) -> bool:
        """
            This method closes connections if they exist.
        """
        ...