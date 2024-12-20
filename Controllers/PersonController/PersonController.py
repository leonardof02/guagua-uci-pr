from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, CallbackContext, filters, ConversationHandler, CommandHandler, MessageHandler

from Controllers.UserController import UserController
from Controllers.PersonController.ConversationStates import ConversationStates

from Constants.CallbackDataActions import Actions
from Models.Person import Person

from Helpers.Validator import Validator
from Helpers.Helper import Helper

# Person Management Controller


class PersonController:

    ### Getting Persons ###
    @staticmethod
    async def get_persons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.delete()
        persons_reply_markup, answer = Helper.get_persons_keyboard_from_user(
            update, context)
        await update.message.reply_text(answer, parse_mode="Markdown")
        return ConversationHandler.END

    ### Creating Persons ###

    #  Create a person when /new command
    @staticmethod
    async def start_register_person(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.delete()
        full_name = update.effective_user.full_name
        await update.message.reply_text(
            f"Hola {
                full_name} por favor inserte el nombre de la persona que quieres agregar para anotarse: ",
        )
        return ConversationStates.GET_CI_OF_PERSON

    # GET_CI_OF_PERSON
    # (from Start Register Person, and get person name) -> (to Get Person CI)
    @staticmethod
    async def get_person_ci(update: Update, context: ContextTypes.DEFAULT_TYPE):
        person_name = update.message.text

        if (not Validator.is_name(person_name)):
            await update.message.reply_text("🛑 Nombre no válido, operacion cancelada", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        context.user_data["person_name"] = person_name
        await update.message.reply_text(
            f"🪪 Inserte el # de Carné de identidad de la persona 👇 (para evitar anotaciones duplicadas): ",
        )
        return ConversationStates.GET_LOCATION

    # REGISTER_PERSON
    @staticmethod
    async def register_person(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        person_name = context.user_data.get("person_name")
        person_ci = context.user_data.get("person_ci")
        person_location = update.message.text

        if (not Validator.is_name(person_location)):
            await update.message.reply_text("🛑 Nombre no válido, operacion cancelada", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        Person.create_person(person_ci, person_name, person_location,
                             update.effective_user.id)
        await update.message.reply_text(f"✅ Persona agregada con exito!: {person_name}")
        context.user_data.clear()
        return ConversationHandler.END

    # CANCEL_OPERATION
    @staticmethod
    async def cancel_operations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data.clear()
        await update.message.reply_text("Operacion Cancelada", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    #### Editing Persons ###

    #  Show persons to edit when /edit command
    @staticmethod
    async def get_persons_for_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        await update.message.delete()
        persons_reply_markup, answer = Helper.get_persons_keyboard_from_user(
            update, context)

        await update.message.reply_text(
            f"*✏️ Selecciona el nombre de la persona que quieres editar:* \n\n{
                answer}",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(
                persons_reply_markup, one_time_keyboard=True,
                input_field_placeholder="Nombre de la persona"
            ))
        return ConversationStates.START_EDIT_PERSON

    # START_EDIT_PERSON
    @staticmethod
    async def get_person_name_for_edit(update: Update, context: CallbackContext):
        await update.message.delete()
        person_name = update.message.text

        if (not Validator.is_name(person_name)):
            await update.message.reply_text("🛑 Nombre no válido, operacion cancelada", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        person = Person.get_person_ci_by_name_from_telegram_id(
            update.effective_user.id, person_name)

        if (not person):
            await update.message.reply_text("🛑 No existe esa persona, operacion cancelada", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        (pk,) = person
        context.user_data["pk"] = pk
        await update.message.reply_text("🔤 Inserte el nombre y apellido de la persona: ", reply_markup=ReplyKeyboardRemove())
        return ConversationStates.GET_CI_OF_PERSON

    # GET_LOCATION
    # (from Get Person CI) -> (to Get Person Location)
    @staticmethod
    async def get_person_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
        person_ci = update.message.text

        if (not Validator.is_valid_ci(person_ci)):
            await update.message.reply_text("🛑 Carné de identidad no válido, debe tener 11 dígitos consecutivos, operacion cancelada", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        # Check if CI person already exists
        created_persons = Person.get_all_persons_by_telegram_id(
            update.effective_user.id)
        for person in created_persons:
            (ci, name, location) = person
            if (ci == person_ci):
                await update.message.reply_text(f"🛑 Ya tienes una persona registrada con el carne de identidad: {ci}", reply_markup=ReplyKeyboardRemove())
                return ConversationHandler.END
            
        context.user_data["person_ci"] = update.message.text
        await update.message.reply_text("🗺️ Inserte el puente de recogida/bajada de la guagua: ", reply_markup=ReplyKeyboardRemove())
        if (context.user_data.get("pk")):
            return ConversationStates.EDIT_PERSON
        else:
            return ConversationStates.REGISTER_PERSON

    # EDIT_PERSON
    @staticmethod
    async def edit_person(update: Update, context: CallbackContext):
        person_location = update.message.text

        if (not Validator.is_name(person_location)):
            await update.message.reply_text("🛑 Nombre no válido, operacion cancelada", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        person_name = context.user_data.get("person_name")
        pk = context.user_data.get("pk")
        Person.edit_person_name_by_pk(pk, person_location, person_name)
        await update.message.reply_text(f"✅ Persona editada con exito!: {person_name}", reply_markup=ReplyKeyboardRemove())
        context.user_data.clear()
        return ConversationHandler.END

    #### Remove Persons ###

    #  Delete person when /delete
    @staticmethod
    async def get_persons_for_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        await update.message.delete()
        persons_reply_markup, answer = Helper.get_persons_keyboard_from_user(
            update, context)

        await update.message.reply_text(
            f"*🗑️ Selecciona el nombre de la persona a borrar:* \n\n{answer}",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(
                persons_reply_markup,
                one_time_keyboard=True,
                input_field_placeholder="Nombre de la persona",
            ))

        return ConversationStates.DELETE_PERSON

    # DELETE_PERSON
    @staticmethod
    async def delete_person(update: Update, context: CallbackContext):

        await update.message.delete()
        person_name = update.message.text
        person = Person.get_person_ci_by_name_from_telegram_id(
            update.effective_user.id, person_name)

        if (not person):
            await update.message.reply_text("🛑 No existe esa persona", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        Person.delete_person_by_name_from_telegram_id(
            update.effective_user.id, update.message.text)
        await update.message.reply_text(f"✅ Persona borrada con exito!: {person_name}", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


person_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("mis_personas", PersonController.get_persons),
        CommandHandler("nueva_persona",
                       PersonController.start_register_person),
        CommandHandler("editar_persona",
                       PersonController.get_persons_for_edit),
        CommandHandler("borrar_persona",
                       PersonController.get_persons_for_delete),
    ],
    states={
        ConversationStates.REGISTER_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.register_person)],
        ConversationStates.START_EDIT_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.get_person_name_for_edit)],
        ConversationStates.EDIT_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.edit_person)],
        ConversationStates.DELETE_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.delete_person)],
        ConversationStates.GET_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.get_person_location)],
        ConversationStates.GET_CI_OF_PERSON: [MessageHandler(filters.TEXT & ~filters.COMMAND, PersonController.get_person_ci)],
    },
    fallbacks=[CommandHandler("cancelar", PersonController.cancel_operations), MessageHandler(
        filters.COMMAND, PersonController.cancel_operations)],
)
