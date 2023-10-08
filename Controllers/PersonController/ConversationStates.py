from enum import Enum

class ConversationStates(Enum):
    CANCEL_OPERATION = 0
    REGISTER_PERSON = 1
    START_EDIT_PERSON = 2
    EDIT_PERSON = 3
    DELETE_PERSON = 4