from telegram import Update, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, filters, ConversationHandler, CommandHandler, MessageHandler

from typing import Sequence

from Models.User import User
from Models.Person import Person

# Person Management Controller
class PersonController:

    # Conversation states
    conversation_states = {
        "GET_PERSON_NAME": 1,
        "CANCEL_OPERATION": 2
    }

    @staticmethod
    async def get_persons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        persons = Person.get_all_persons_by_telegram_id(update.effective_user.id)
        print(persons)
        persons_reply_markup: Sequence[Sequence[InlineKeyboardButton]] = [[]]
        for person in persons:
            (name,) = person
            persons_reply_markup.append([InlineKeyboardButton(text=name, callback_data=name)])

        await update.message.reply_text("Tus personas", reply_markup=InlineKeyboardMarkup(persons_reply_markup))

    # Create a person when /new command
    @staticmethod
    async def start_register_person(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        full_name = update.effective_user.full_name

        await update.message.reply_text(
            f"Hola {full_name} por favor inserte el nombe de la persona que quieres agregar para anotarse",
        )
        return PersonController.conversation_states["GET_PERSON_NAME"]
    
    @staticmethod
    async def get_person_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        Person.create_person( update.message.text, update.effective_user.id )
        await update.message.reply_text(f"Persona agregada con exito: {update.message.text}")
        return ConversationHandler.END
    
    @staticmethod
    async def cancel_operations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text( "Operacion Cancelada" )
        return ConversationHandler.END


    register_person_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("new", start_register_person)],
        states={
            conversation_states["GET_PERSON_NAME"]: [MessageHandler(filters.TEXT, get_person_name)]
        },
        fallbacks=[CommandHandler("cancel", cancel_operations)]
    )