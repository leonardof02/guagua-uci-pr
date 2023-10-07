from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler

from Bot import *

from Controllers.ReservationController import ReservationController
from Controllers.PersonController import PersonController
from Controllers.AdminController import AdminController
from Controllers.UserController import UserController

from CallbackQueryObjects.Router import Router

def main() -> None:
    guagua_pr_bot = Bot()

    # Commands
    guagua_pr_bot.application.add_handlers([
        CommandHandler("start", UserController.register_user ),
        CommandHandler("reservar", ReservationController.create_reservation ),
        CommandHandler("forward", AdminController.forward_message ),
        CommandHandler("personas", PersonController.get_persons)
    ])
    
    # Conversation Handler
    guagua_pr_bot.application.add_handler( PersonController.register_person_conv_handler )

    # Callback Query Router
    guagua_pr_bot.application.add_handler(CallbackQueryHandler( Router.defineRoutes ))

    # Run Bot
    guagua_pr_bot.run()


if __name__ == "__main__":
    main()