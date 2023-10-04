import pathlib

from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes, CallbackContext

from Models.User import User
from Constants.Env import ASSETS_PATH

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
            reply_text = f"""🛑 Para el correcto funcionamiento del bot es necesario que se cree su username:\n
            Vaya a ajustes de su perfil y creese un username unico por favor.
            """
            img_path = pathlib.Path(ASSETS_PATH).resolve();
            await update.message.reply_photo(photo=(open(img_path, "+rb")), caption=reply_text)
            return

        if User.exists(user_id):
            await update.message.delete()
            await update.message.reply_text(rf"ℹ️ El usuario: {full_name} (@{username}) ya esta registrado")
            return
        
        User.create_user(user_id, username, chat_id, full_name)
        await update.message.reply_text(rf"✅ El usuario: {full_name} (@{username}) fue registrado satisfactoriamente")