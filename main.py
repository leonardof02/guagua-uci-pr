from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler

from Bot import *

from Controllers.ReservationController import ReservationController, reservation_conversation_handler, reservation_callback_query
from Controllers.PersonController.PersonController import PersonController, person_conversation_handler
from Controllers.AdminController import AdminController
from Controllers.UserController import UserController

def main() -> None:
    guagua_pr_bot = Bot()

    # Commands
    guagua_pr_bot.application.add_handlers([
        CommandHandler("start", UserController.register_user ),
        CommandHandler("forward", AdminController.forward_message ),
    ])
    
    # Conversation Handlers
    guagua_pr_bot.application.add_handler( person_conversation_handler )
    guagua_pr_bot.application.add_handler( reservation_conversation_handler )

    # Callback Query Handlers
    guagua_pr_bot.application.add_handler( reservation_callback_query )

    # Run Bot
    guagua_pr_bot.run()


if __name__ == "__main__":
    main()