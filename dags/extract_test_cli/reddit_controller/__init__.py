import os
from dotenv import load_dotenv
load_dotenv()

USERNAME_REDDIT = os.getenv("USERNAME")
PASSWORD_REDDIT = os.getenv("PASSWORD")
CLIENT_ID_REDDIT = os.getenv("CLIENT_ID")
CLIENT_SECRET_REDDIT = os.getenv("CLIENT_SECRET")
USER_AGENT_REDDIT = os.getenv("USER_AGENT")
REDDIT_SOURCE = "REDDIT"
