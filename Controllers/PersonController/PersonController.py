from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, CallbackContext, filters, ConversationHandler, CommandHandler, MessageHandler

from typing import Sequence

from Controllers.PersonController.ConversationStates import ConversationStates

from Constants.CallbackDataActions import Actions
from Models.Person import Person
from Helpers.Helper import Helper

# Person Management Controller
class PersonController:

    ### Getting Persons ###
    @staticmethod
    async def get_persons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        persons_reply_markup, answer = PersonController.get_persons_keyboard(update, context)
        await update.message.reply_text(answer, parse_mode="Markdown")
        return ConversationHandler.END

    ### Creating Persons ###

    #  Create a person when /new command
    @staticmethod
    async def start_register_person(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        full_name = update.effective_user.full_name
        await update.message.reply_text(
            f"Hola {full_name} por favor inserte el nombe de la persona que quieres agregar para anotarse: ",
        )
        return ConversationStates.GET_LOCATION

    # REGISTER_PERSON
    @staticmethod
    async def register_person(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        person_name = context.user_data.get("person_name")
        person_location = update.message.text
        Person.create_person(person_name, person_location, update.effective_user.id)
        await update.message.reply_text(f"✅ Persona agregada con exito!: {person_name}")
        context.user_data.clear()
        return ConversationHandler.END
    
    # CANCEL_OPERATION
    @staticmethod
    async def cancel_operations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.clear()
        await update.message.reply_text( "Operacion Cancelada", reply_markup=ReplyKeyboardRemove() )
        return ConversationHandler.END
    
    #### Editing Persons ###

    #  Show persons to edit when /edit command
    @staticmethod
    async def get_persons_for_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        persons_reply_markup, answer = PersonController.get_persons_keyboard(update, context)

        await update.message.reply_text(
            f"*✏️ Selecciona el nombre de la persona que quieres editar:* \n\n{answer}",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(
                persons_reply_markup , one_time_keyboard=True,
                input_field_placeholder="Tus personas"
                ))
        return ConversationStates.START_EDIT_PERSON

    # START_EDIT_PERSON
    @staticmethod
    async def get_person_name_for_edit(update: Update, context: CallbackContext):
        person_name = update.message.text
        (pk,) = Person.get_person_id_by_name_from_telegram_id(update.effective_user.id, person_name)
        context.user_data["pk"] = pk
        await update.message.reply_text("Inserte el nombre nuevo de la persona: ", reply_markup=ReplyKeyboardRemove())
        return ConversationStates.GET_LOCATION
    
    @staticmethod
    async def get_person_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["person_name"] = update.message.text
        await update.message.reply_text("🗺️ Inserte el municipio de la persona: ", reply_markup=ReplyKeyboardRemove())
        if (context.user_data.get("pk")):
            return ConversationStates.EDIT_PERSON
        else:
            return ConversationStates.REGISTER_PERSON
    
    # EDIT_PERSON
    @staticmethod
    async def edit_person(update: Update, context: CallbackContext):
        person_location = update.message.text
        person_name = context.user_data.get("person_name")
        pk = context.user_data.get("pk")
        Person.edit_person_name_by_pk(pk, person_location, person_name)
        await update.message.reply_text(f"✅ Persona editada con exito!: {person_name}")
        context.user_data.clear()
        return ConversationHandler.END
    
    #### Remove Persons ###

    #  Delete person when /delete
    @staticmethod
    async def get_persons_for_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        persons_reply_markup, answer = PersonController.get_persons_keyboard(update, context)

        await update.message.reply_text(
            f"*🗑️ Selecciona el nombre de la persona a borrar:* \n\n{answer}",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(
                persons_reply_markup,
                one_time_keyboard=True,
                input_field_placeholder="Tus personas",
                ))
        
        return ConversationStates.DELETE_PERSON
    
    # DELETE_PERSON
    @staticmethod
    async def delete_person(update: Update, context: CallbackContext):
        person_name = update.message.text
        Person.delete_person_by_name_from_telegram_id(update.effective_user.id, update.message.text)
        await update.message.reply_text(f"Persona borrada con exito!: {person_name}", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    
    ### Helpers ###

    def get_persons_keyboard(update: Update, context: CallbackContext):
        persons = Person.get_all_persons_by_telegram_id(update.effective_user.id)
        persons_reply_markup: Sequence[Sequence[str]] = [[]]
        answer = "*📜 Personas registradas:* \n------------------------------------------\n"
        
        for person in persons:
            (id, name, location) = person
            button_text = f"{name}"
            persons_reply_markup.append([button_text])
            answer += f"🚹 - {name} | 🗺️ Municipio: {location}\n"

        persons_reply_markup.append(["/cancelar ❌"])
        
        if( len(persons) == 0 ):
            answer = "🚧 *No tienes personas registradas*"
        return persons_reply_markup, answer

    
person_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("list", PersonController.get_persons),
        CommandHandler("new", PersonController.start_register_person),
        CommandHandler("edit", PersonController.get_persons_for_edit),
        CommandHandler("delete", PersonController.get_persons_for_delete),
    ],
    states={
        ConversationStates.REGISTER_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.register_person)],
        ConversationStates.START_EDIT_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.get_person_name_for_edit)],
        ConversationStates.EDIT_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.edit_person)],
        ConversationStates.DELETE_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.delete_person)],
        ConversationStates.GET_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.get_person_location)],
    },
    fallbacks=[CommandHandler("cancelar", PersonController.cancel_operations)],
)