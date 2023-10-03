from telegram import Update
from telegram.ext import ContextTypes

from Models.User import User

# Create a user when /start the bot
async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    full_name = update.message.from_user.full_name

    if( not username ):
        await update.message.reply_text(rf"🛑 Por favor creese su nombre de usuario y regrese luego")
        return

    if User.exists(user_id):
        await update.message.reply_text(rf"ℹ️ El usuario: {full_name} (@{username}) ya esta registrado")
        return
    
    User.create_user(user_id, username, full_name)
    await update.message.reply_text(rf"✅ El usuario: {full_name} (@{username}) fue registrado satisfactoriamente")