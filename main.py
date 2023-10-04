from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, filters

from Bot import *

from Controllers.ReservationController import ReservationController
from Controllers.UserController import UserController
from Controllers.AdminController import AdminController

from CallbackQueryRouter.Router import Router

def main() -> None:
    guagua_pr_bot = Bot()

    # Commands
    guagua_pr_bot.application.add_handler(CommandHandler("start", UserController.register_user ))
    guagua_pr_bot.application.add_handler(CommandHandler("reservar", ReservationController.create_reservation ))
    guagua_pr_bot.application.add_handler(CommandHandler("forward", AdminController.forward_message ))

    # Callback Query Router
    guagua_pr_bot.application.add_handler(CallbackQueryHandler( Router.defineRoutes ))

    # Run Bot
    guagua_pr_bot.run()


if __name__ == "__main__":
    main()