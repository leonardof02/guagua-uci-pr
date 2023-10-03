from telegram import Update, CallbackQuery
from telegram.ext import CallbackContext

from Constants.CallbackData import CANCEL_RESERVATION
from Controllers.UserController import UserController
from Controllers.ReservationController import ReservationController

class Router:
    """Class for redirecting `callback data` from Markups to respective controllers"""

    # Callback data actions name and functions to execute
    ACTIONS = {
        CANCEL_RESERVATION: ReservationController.cancel_reservation
    }

    # Redirect callback action to respective functions
    async def defineRoutes(update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        action = query.data

        if( Router.ACTIONS[action] ):
            await Router.ACTIONS[action](update, context, query)