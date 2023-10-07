import logging
from telegram import Update
from telegram.ext import Application

from Models.User import User
from Models.Reservation import Reservation
from Models.Person import Person

from Constants.Env import TOKEN, ID_ADMIN

class Bot:

    application: Application
    logger: logging.Logger
    
    def __init__(self):
        self.config()
        self.application = Application.builder().token(TOKEN).build()

    
    def config(self):
        self.initDB()
        self.set_logger()

    def initDB(self):
        User.create_table()
        Person.create_table()
        Reservation.create_table()

    def set_logger(self):
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)