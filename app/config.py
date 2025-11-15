import os
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("ACCESS_KEY")
UNSPLASH_API = "https://api.unsplash.com"