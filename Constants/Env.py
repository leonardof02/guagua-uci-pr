import dotenv, os

# .env variables
dotenv.load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ID_ADMIN = int(os.getenv("ID_ADMIN"))
ASSETS_PATH = os.getenv("ASSETS_PATH")