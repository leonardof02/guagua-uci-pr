from telegram import Update
from telegram.ext import ContextTypes

from Models.Reservation import Reservation

# Reservation management controller
class ReservationController:

    # Create a unique reservation by User
    async def create_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        user_id = update.message.from_user.id
        username = update.message.from_user.username
        full_name = update.message.from_user.full_name

        reservation = Reservation.findByUserId(user_id)

        if( reservation ):
            # Number of arrival
            arrival_order = Reservation.getArrivalOrderByUser(user_id);
            await update.message.reply_text(f"⏱️ Ya usted reservo: {full_name} @{username}) \n 🔢 Turno: {arrival_order}")
            return

        new_reservation = Reservation.create_reservation(user_id)
        await update.message.reply_text(f"✅🆕 Se ha creado una reservacion para usted: {full_name} (@{username}) \n Turno #{new_reservation}")