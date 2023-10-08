import json

class Helper:

    @staticmethod
    def is_json(string: str) -> bool:
        try:
            json.loads(string)
            return True
        except:
            return False