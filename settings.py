import os
from pathlib import Path

from dotenv import load_dotenv


CURRENT_PATH = Path(__file__).resolve().parent
load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_NAME = os.getenv("DB_NAME")

DB_FILE_PATH = CURRENT_PATH / DB_NAME

PRODUCTS_PER_PAGE = 5
