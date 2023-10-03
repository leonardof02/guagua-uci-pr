from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext

from Models.Reservation import Reservation
from Constants.CallbackData import CANCEL_RESERVATION

# Reservation management controller
class ReservationController:

    # UI Elements
    cancel_reservation_button = InlineKeyboardButton("🚫 Cancelar Reservacion", callback_data=CANCEL_RESERVATION);
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

        new_reservation = Reservation.create_reservation(user_id)
        await update.message.reply_text(
            f"✅🆕 Se ha creado una reservacion para usted: {full_name} (@{username}) \n Turno #{new_reservation}",
            reply_markup=ReservationController.cancel_reservation_markup
        )

    @staticmethod
    async def cancel_reservation(update: Update, context: CallbackContext):
        pass