from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters
from datetime import datetime

from Bot import *

from Controllers.ReservationController import ReservationController
from Controllers.UserController import UserController

def main() -> None:
    guagua_pr_bot = Bot()

    # Commands
    guagua_pr_bot.application.add_handler(CommandHandler("start", UserController.register_user ))
    guagua_pr_bot.application.add_handler(CommandHandler("reservar", ReservationController.create_reservation ))
    
    # Filters
    guagua_pr_bot.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, None))

    # Run Bot
    guagua_pr_bot.application.run_polling(allowed_updates=Update.ALL_TYPES)
    guagua_pr_bot.run()


if __name__ == "__main__":
    main()