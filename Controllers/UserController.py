import pathlib

from telegram import Update
from telegram.ext import ContextTypes

from Models.User import User
from Constants import ASSETS_PATH

# User management controller
class UserController:

    # Create a user when /start the bot
    async def register_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        full_name = update.message.from_user.full_name

        if( not username ):
            reply_text = f"""🛑 Para el correcto funcionamiento del bot es necesario que se cree su username:\n
            Vaya a ajustes de su perfil y creese un username unico por favor.
            """
            img_path = pathlib.Path(ASSETS_PATH).resolve();
            await update.message.reply_photo(photo=(open(img_path, "+rb")), caption=reply_text)
            return

        if User.exists(user_id):
            await update.message.reply_text(rf"ℹ️ El usuario: {full_name} (@{username}) ya esta registrado")
            return
        
        User.create_user(user_id, username, full_name)
        await update.message.reply_text(rf"✅ El usuario: {full_name} (@{username}) fue registrado satisfactoriamente")