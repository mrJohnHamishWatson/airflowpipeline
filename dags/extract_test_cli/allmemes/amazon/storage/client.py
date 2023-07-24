import boto3

from allmemes.amazon import AWS_ACCESS_KEY, AWS_SECRET_KEY


class S3Client:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
        )
