
#ABC -> Abstract Base Class

class InputValidation():

    @staticmethod
    def validate_input(input_value: str, **kwargs: any) -> bool:
        """
            This is a static method that can be inherited by any class that needs to validate input. It could've just been 
            a static class, but too late to change now.

            :params: Caller must provide the input value along with keyword arguments: char_input, integer_input, or string_input set to True,
            and if char_input, then provide a string containing valid characters as valid_input.
            :return: Returns a boolean value, true if valid input, false if not valid.
        """
        if kwargs.get('char_input') != None:
            return len(input_value) == 1 and input_value in kwargs['valid_input']
        elif kwargs.get('integer_input') != None:
            return input_value.isdigit()
        elif kwargs.get('string_input') != None:
            return input_value.isalpha() and len(input_value) > 2
        elif kwargs.get('credential_input') != None:
            alpha = False
            numeric = False
            space = False
            for char in input_value:
                if not alpha:
                    alpha = char.isalpha()
                if not numeric:
                    numeric = char.isdigit()
                if not space:
                    space = char.isspace()
            valid = (alpha and numeric and not space) #contains at least a letter and a number, but cannot have any whitespace.
            return valid and len(input_value) > 4
        else:
            return False