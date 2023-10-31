from telegram.ext import CommandHandler, MessageHandler, filters

from Bot import *

from Controllers.ReservationController.ReservationController import reservation_conversation_handler, reservation_callback_query
from Controllers.PersonController.PersonController import person_conversation_handler

from Controllers.UserController import UserController
from Controllers.AdminController import AdminController
from Controllers.HelpController import Tutorial

def main() -> None:
    guagua_pr_bot = Bot()

    # Commands
    guagua_pr_bot.application.add_handlers([
        CommandHandler("start", UserController.register_user),
        CommandHandler("tutorial", Tutorial.get_tutorial),

        # Admin Commands
        CommandHandler("clean", AdminController.clean),
        CommandHandler("forward", AdminController.forward_message ),
        CommandHandler("forward_clean", AdminController.forward_message_and_clean_reservations ),
        CommandHandler("get_listado", AdminController.get_list_reservation),
        CommandHandler("ver_lista", AdminController.get_list_reservation_file),
        CommandHandler("puentes", AdminController.get_locations)
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