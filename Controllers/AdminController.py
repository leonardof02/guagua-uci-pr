from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes, CallbackContext

from Constants.Env import ID_ADMIN
from Models.User import User
from Models.Reservation import Reservation

class AdminController:

    # Verify if this user is admin
    @staticmethod
    def is_from_admin(user_id) -> bool:
        return user_id == ID_ADMIN
    
    async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        id = update.effective_user.id
        if( not AdminController.is_from_admin(id) ):
            return
        for chat_id in User.get_all_users_chat_id():
            (user_id,) = chat_id
            await context.bot.send_message( chat_id=user_id, text=update.message.text.removeprefix("/forward "))

    async def forward_message_and_clean_reservations(update: Update, context: ContextTypes.DEFAULT_TYPE):
        id = update.effective_user.id
        if( not AdminController.is_from_admin(id) ):
            return
        
        Reservation.clean()
        for chat_id in User.get_all_users_chat_id():
            (user_id,) = chat_id
            await context.bot.send_message( chat_id=user_id, text=update.message.text.removeprefix("/forward_clean "))

    async def get_list_reservation(update: Update, context: ContextTypes.DEFAULT_TYPE):
        all_reservation = Reservation.get_all_reservations()
        answer = "🟩 Listado de reservas \nOrden | Nombre | Puente | Reservado por \n --------------------------------------------------\n"
        for reservation in all_reservation:
            order, name, location, reserved_by = reservation
            answer += f"{order} - {name} | Puente: {location}: por {reserved_by}\n"
        await update.message.reply_text(answer, parse_mode="Markdown")