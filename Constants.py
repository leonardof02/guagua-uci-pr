import dotenv, os

dotenv.load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ID_ADMIN = int(os.getenv("ID_ADMIN"))