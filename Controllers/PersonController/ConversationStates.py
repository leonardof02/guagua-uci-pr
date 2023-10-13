from enum import Enum

class ConversationStates(Enum):
    CANCEL_OPERATION = 0
    REGISTER_PERSON = 1
    GET_LOCATION = 2
    START_EDIT_PERSON = 3
    EDIT_PERSON = 4
    DELETE_PERSON = 5