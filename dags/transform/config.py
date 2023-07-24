import os

from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AAA_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AAA_SECRET_ACCESS_KEY")

BUCKET_NAME_METADATA = "metadatabucketttt"
BUCKET_NAME_IMAGE = "newimagebuckettest"