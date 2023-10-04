from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes, CallbackContext

from Constants.Env import ID_ADMIN
from Models.User import User

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