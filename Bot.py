import logging
from telegram import Update
from telegram.ext import Application

from Constants import TOKEN, ID_ADMIN

class Bot:

    application: Application
    logger: logging.Logger

    def __init__(self):
        self.config()
        self.application = Application.builder().token(TOKEN).build()

    @staticmethod
    def is_from_admin(update: Update):
        return update.message.from_user.id == ID_ADMIN
    
    def config(self):
        self.set_logger()

    def set_logger(self):
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

    def run(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        print("Bot running... " +  self.TOKEN )