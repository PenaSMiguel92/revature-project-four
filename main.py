from implementation.main_menu import MainMenu, menu_state
from custom_exceptions.menu_selection_invalid import MenuSelectionInvalidException
from custom_exceptions.connection_failed import ConnectionFailed
from custom_exceptions.table_selection_invalid import TableSelectionInvalidException

def main():
    menu = MainMenu()
    while menu.get_state() != menu_state.CLOSING_STATE:
        try:
            menu.run()
        except (MenuSelectionInvalidException, ConnectionFailed, TableSelectionInvalidException) as e:
            print(e.message)

    print('Goodbye!')
    # menu.close_connections()

if __name__ == '__main__':
    main()

