import json
from typing import Sequence

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from Controllers.ReservationController.ConversationStates import ConversationStates

from Models.Reservation import Reservation
from Models.Person import Person
from Helpers.Helper import Helper

# Reservation management controller
class ReservationController:

    @staticmethod
    async def select_person_for_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        persons = Person.get_all_persons_by_telegram_id( telegram_id )
        persons_reply_markup: Sequence[Sequence[str]] = [[]]
        answer = "*✒️ A que persona vas a reservar?:* \n------------------------------------------\n"
        
        for person in persons:
            (id, name) = person
            button_text = f"{name}"
            persons_reply_markup.append([button_text])
            answer += f"🚹 - {name}\n"

        persons_reply_markup.append(["/cancelar ❌"])
        
        if( len(persons) == 0 ):
            answer = "🚧 *No existen reservas*"
        
        await update.message.reply_text(answer, parse_mode="Markdown", reply_markup=ReplyKeyboardMarkup(persons_reply_markup))
        return ConversationStates.CREATE_RESERVATION



    @staticmethod
    async def get_reservations(update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        reservations = Reservation.get_all_reservations_by_telegram_id(telegram_id)

        if(not reservations):
            await update.message.reply_text("🚧 *No tienes personas registradas*", parse_mode="Markdown")
            return

        for reservation in reservations:
            ( reservation_id, arrival_order, name) = reservation
            action = { "name": "CANCEL_RESERVATION", "pk": reservation_id }
            cancel_reservation_button = InlineKeyboardButton("🚫🚌 Cancelar", callback_data=json.dumps(action))
            await update.message.reply_text(
                f"🪪 {name}\n*🔢 Turno:* {arrival_order}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([[cancel_reservation_button]])
            )

    @staticmethod
    async def create_reservation_for_all_person(update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        persons = Person.get_all_persons_by_telegram_id( telegram_id )
        for person in persons:
            id, name = person
            if( not Reservation.exist_person(id) ):
                Reservation.create_reservation( telegram_id, id )
        await update.message.reply_text("✅ Todas las personas han sido reservadas con exito!")
        await ReservationController.get_reservations(update, context)

    # Create a unique reservation by User
    @staticmethod
    async def create_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        telegram_id = update.message.from_user.id
        person_name = update.message.text

        person = Person.get_person_id_by_name_from_telegram_id(telegram_id, person_name)

        if(not person):
            await update.message.reply_text(f"🫤 Lo siento, no hay personas registradas con el nombre {person_name}", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        
        person_id, = person
        if( not Reservation.exist_person(person_id) ):
            Reservation.create_reservation(telegram_id, person_id)
            await update.message.reply_text(f"✅ Se ha creado una reserva satisfactoriamente para: {person_name}", reply_markup=ReplyKeyboardRemove())
        else:
            await update.message.reply_text("😉 Ya esa persona estaba reservada: ", reply_markup=ReplyKeyboardRemove())
        reservation_id, arrival_order, name = Reservation.get_reservation_by_user_id_and_name(telegram_id, person_name)

        action = { "name": "CANCEL_RESERVATION", "pk": reservation_id }
        cancel_reservation_button = InlineKeyboardButton("🚫🚌 Cancelar", callback_data=json.dumps(action))

        await update.message.reply_text(
            f"🪪 {person_name}\n*🔢 Turno:* {arrival_order}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[cancel_reservation_button]])
        )
        return ConversationHandler.END

    @staticmethod
    async def cancel_reservation(update: Update, context: CallbackContext):
        await update.effective_message.delete()
        action = update.callback_query.data

        if( not Helper.is_json( action ) ):
            return

        name, pk = json.loads(action).values()

        if( name != "CANCEL_RESERVATION" ):
            return

        reservation_id, arrival_order, name = Reservation.get_reservation_by_id(pk)
        Reservation.delete_by_id(reservation_id)
        await update.effective_message.reply_text(f"✅ La reservacion de {name} se ha cancelado con exito ! \n 🗑️ Eliminado el turno: {arrival_order}")

    # CANCEL_OPERATION
    @staticmethod
    async def cancel_operations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text( "Operacion Cancelada", reply_markup=ReplyKeyboardRemove() )
        return ConversationHandler.END

reservation_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler("reservas", ReservationController.get_reservations),
        CommandHandler("reservar_todos", ReservationController.create_reservation_for_all_person),
        CommandHandler("reservar", ReservationController.select_person_for_reservation)
    ],
    states={
        ConversationStates.CREATE_RESERVATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, ReservationController.create_reservation)]
    },
    fallbacks=[ CommandHandler("cancel", ReservationController.cancel_operations) ]
)

reservation_callback_query = CallbackQueryHandler(ReservationController.cancel_reservation)