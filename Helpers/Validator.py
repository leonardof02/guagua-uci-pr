import re

class Validator:

    @staticmethod
    def is_name(string: str):
        name_regex = r"^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$"
        if( re.match( name_regex, string ) ):
            return True
        return False
