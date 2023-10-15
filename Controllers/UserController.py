import pathlib

from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes, CallbackContext

from Models.User import User
from Constants.Env import ASSETS_PATH
from Controllers.HelpController import Tutorial

# User management controller
class UserController:

    # Create a user when /start the bot
    @staticmethod
    async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        user_id = update._effective_user.id
        username = update.effective_user.username
        full_name = update.effective_user.full_name
        chat_id = update.effective_chat.id

        if( not username ):
            username = "No tiene"

        if User.exists(user_id):
            await update.message.delete()
            await update.message.reply_text(rf"ℹ️ El usuario: {full_name} (@{username}) ya esta registrado")
            return
        
        User.create_user(user_id, username, chat_id, full_name)
        await update.message.reply_text(rf"✅ El usuario: {full_name} (@{username}) fue registrado satisfactoriamente")
        await Tutorial.get_tutorial(update, context)