from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import ContextTypes, CallbackContext

from Models.Reservation import Reservation
from Constants.CallbackData import CANCEL_RESERVATION

# Reservation management controller
class ReservationController:

    # UI Elements
    cancel_reservation_button = InlineKeyboardButton("🚫🚌 Cancelar Reservacion", callback_data=CANCEL_RESERVATION);
    cancel_reservation_markup = InlineKeyboardMarkup([[cancel_reservation_button]])

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

        user_id = update.effective_user.id
        full_name = update.effective_user.full_name

        if( not Reservation.existsByUserId(user_id) ):
            await update.effective_message.reply_text(f"😟 Lo siento {full_name}, usted no ha reservado aun")
            return

        arrival_order = Reservation.getArrivalOrderByUser(user_id)
        Reservation.deleteByUserId(user_id)

        await update.effective_message.reply_text(f"✅ Su reservacion se ha cancelado con exito {full_name}! \n 🗑️ Eliminado el turno: {arrival_order}")