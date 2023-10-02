import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from Bot import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if( Bot.is_from_admin(update) ):
        await update.message.reply_text("Hola Leo")
    await update.message.reply_text( rf"Hola { update.message.from_user.name } tu id es: {update.message.from_user.id}" );

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text( update.message.text );

def main() -> None:
    guagua_pr_bot = Bot()
    guagua_pr_bot.application.add_handler(CommandHandler("start", start))
    guagua_pr_bot.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    guagua_pr_bot.application.run_polling(allowed_updates=Update.ALL_TYPES)
    guagua_pr_bot.run()


if __name__ == "__main__":
    main()