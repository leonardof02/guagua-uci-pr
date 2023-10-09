import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler, CommandHandler, CallbackQueryHandler

from Models.Reservation import Reservation
from Models.Person import Person
from Helpers.Helper import Helper

# Reservation management controller
class ReservationController:

    @staticmethod
    async def get_reservations(update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        reservations = Reservation.get_all_reservations_by_telegram_id(telegram_id)
        for reservation in reservations:
            ( reservation_id, arrival_order, name) = reservation
            action = { name: "CANCEL_RESERVATION", "pk": reservation_id }
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

    # Create a unique reservation by User
    @staticmethod
    async def create_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        user_id = update.message.from_user.id
        username = update.message.from_user.username
        full_name = update.message.from_user.full_name

        reservation = Reservation.findByUserId(user_id)

        if( reservation ):
            # Number of arrival
            arrival_order = Reservation.getArrivalOrderByUser(user_id);
            await update.message.reply_text(
                   f"⏱️ Ya usted reservo: {full_name} |@{username}| \n 🔢 Turno: {arrival_order}",
                    reply_markup=ReservationController.cancel_reservation_markup
            )
            return

        Reservation.create_reservation(user_id)
        arrival_order = Reservation.getArrivalOrderByUser(user_id);
        await update.message.reply_text(
            f"✅🆕 Se ha creado una reservacion para usted: {full_name} (@{username}) \n Turno #{arrival_order}",
            reply_markup=ReservationController.cancel_reservation_markup
        )

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
    ],
    states={},
    fallbacks=[ CommandHandler("cancel", ReservationController.cancel_operations) ]
)

reservation_callback_query = CallbackQueryHandler(ReservationController.cancel_reservation)