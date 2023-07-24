import os
from dotenv import load_dotenv
load_dotenv()

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_CLIENT_ID")
UNSPLASH_SOURCE = "unsplash"
UNSPLASH_URL = "https://api.unsplash.com/search/photos"
