import re

class Validator:

    @staticmethod
    def is_name(string: str):
        name_regex = r"^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$"
        if( re.match( name_regex, string ) ):
            return True
        return False
    
    @staticmethod
    def is_valid_ci(string: str):
        ci_regex = r"^\d{11}$"
        if( re.match( ci_regex, string ) ):
            return True
        return False
