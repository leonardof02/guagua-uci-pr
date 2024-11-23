from telegram import Update
from telegram.ext import ContextTypes
from Models.Person import Person
from typing import Sequence
import json

class Helper:

    @staticmethod
    def is_json(string: str) -> bool:
        try:
            json.loads(string)
            return True
        except:
            return False

    @staticmethod
    def get_persons_keyboard_from_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> tuple[ Sequence[Sequence[str]], str ]:
        persons = Person.get_all_persons_by_telegram_id(update.effective_user.id)
        persons_reply_markup: Sequence[Sequence[str]] = [[]]
        answer = "*📜 Personas registradas:* \n------------------------------------------\n"
        
        for person in persons:
            (ci, name, location) = person
            button_text = f"{name}"
            persons_reply_markup.append([button_text])
            answer += f"🚹 - {name} | 🌉 Puente: {location}\n"

        persons_reply_markup.append(["/cancelar ❌"])
        
        if( len(persons) == 0 ):
            answer = "🚧 *No tienes personas registradas*"
        return persons_reply_markup, answer