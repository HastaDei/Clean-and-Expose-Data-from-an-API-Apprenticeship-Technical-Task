# imports
import os
from dotenv import load_dotenv

# loading url and key from .env
load_dotenv()

API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")