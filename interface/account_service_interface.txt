from abc import abstractmethod
from interface.menu_baseclass import MenuBaseClass

class AccountServiceInterface(MenuBaseClass):
    @abstractmethod
    def account_register(self) -> None:
        """
            Method for registering a new user. It will ask the user for a username and password. 
        """
        ...
    
    @abstractmethod
    def account_login(self) -> None:
        """
            Method for login with existing username. It will ask for the username and password, and validate the password. 
        """
        ...

    @abstractmethod
    def account_greeting(self) -> None:
        """
            Method called when login is successful. 
        """
        ...

    @abstractmethod
    def process_input(self) -> None:
        """
            Method for processing user input.
        """
        ...

    @abstractmethod
    def set_state(self, state: int) -> None:
        """
            Use this to set the state instead of setting it directly.
        """
        ...

    @abstractmethod
    def get_state(self) -> int:
        """
            Use this to get the state instead of accessing it directly.
        """
        ...

    def get_account_role(self) -> bool:
        """
            Use this to get the account's current role.
        """
        ...

    @abstractmethod
    def close_connections(self) -> bool:
        """
            This method closes connections if they exist.
        """
        ...