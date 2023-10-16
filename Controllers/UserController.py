import pathlib

from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes, CallbackContext

from Models.User import User
from Constants.Env import ASSETS_PATH
from Controllers.HelpController import Tutorial

# User management controller
class UserController:

    # Create a user when /start the bot
    async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update._effective_user.id
        full_name = update.effective_user.full_name

        if User.exists(user_id):
            return
        
        User.create_user(user_id, full_name)
        await update.message.reply_text(rf"✅ El usuario: {full_name} fue registrado satisfactoriamente")
        await Tutorial.get_tutorial(update, context)