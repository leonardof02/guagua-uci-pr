from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime
from Models.User import User

from Bot import *

def main() -> None:
    guagua_pr_bot = Bot()
    guagua_pr_bot.application.add_handler(CommandHandler("start", start))
    guagua_pr_bot.application.add_handler(CommandHandler("reservar", reserve))
    guagua_pr_bot.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, None))
    guagua_pr_bot.application.run_polling(allowed_updates=Update.ALL_TYPES)
    guagua_pr_bot.run()


if __name__ == "__main__":
    main()