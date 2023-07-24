import json
from datetime import datetime
from io import BytesIO
from typing import List

# import cv2
import fastavro
import requests

from allmemes.amazon.storage import IMAGE_BUCKET_NAME, METADATA_BUCKET_NAME
from allmemes.amazon.storage.client import S3Client
from allmemes.models.image_model import ImageModel

DEBUG = False


class S3:
    def __init__(self):
        self.repo_s3 = S3Client()

    def upload_meme(self, image: ImageModel):
        try:
            print(f'here is image_url = {image.url}')
            response = requests.get(image.url)
            if response.status_code == 200:
                bytesIO = BytesIO(bytes(response.content))
                with bytesIO as data:
                    self.repo_s3.client.upload_fileobj(data, IMAGE_BUCKET_NAME, image.file_name)
        except Exception as err:
            print(err)

    def upload_memes(self, memes: List[ImageModel]):
        print(f"here is memes = {memes}")
        for meme in memes:
            print(f'here is meme = {meme}')
            self.upload_meme(meme)

    def get_s3_link_by_name(self, photo_name):
        response = self.repo_s3.client.generate_presigned_url("get_object", Params={'Bucket': IMAGE_BUCKET_NAME,
                                                                                    'Key': photo_name})
        return response
        #response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_name},
        #                                            ExpiresIn=expiration)

    def upload_metadata(self, memes: List[ImageModel]):
        json_list = [meme.to_json() for meme in memes]
        for json_ in json_list:
            json_["url"] = self.get_s3_link_by_name(json_["file_name"])
        print(f'Here is json_list = {json_list}')
        json_file = json.dumps(json_list)
        print(f'here is json_file = {json_file}')
        source = memes[0].source
        print(f'here is source = {source}')
        current_date = datetime.today().strftime('%Y-%m-%d-%H')
        print(f'here is current_date = {current_date}')
        file_name = f"{source}-{current_date}.json"
        self.repo_s3.client.put_object(Bucket=METADATA_BUCKET_NAME, Key=file_name, Body=json_file)

    """
    @staticmethod
    def get_avro_schema():
        return {
            "type": "record",
            "name": "image",
            "namespace": "image.avro",
            "fields": [
                {"name": "source", "type": "string"},
                {"name": "sub_source", "type": "string"},
                {"name": "url", "type": "string"},
                {"name": "caption", "type": "string"}
            ]
        }

    def upload_metadata(self, memes: List[ImageModel]):
        json_list = [meme.to_json() for meme in memes]
        for json_object in json_list:
            print(f'here is json_object = {json_object}')
            for key in json_object.keys():
                print(f'here is key = {key}')
                print(f'here is value = {json_object[key]}')
                if isinstance(json_object.get(key), str):
                    print('HERE IS ERROR INTO AVRO WRITING')
                    json_object[key] = "MOCK FILE ERROR"
        print(f'Here is json_list = {json_list}')
        source = memes[0].source
        print(f'here is source = {source}')
        current_date = datetime.today().strftime('%Y-%m-%d-%H')
        print(f'here is current_date = {current_date}')
        file_name = f"{source}-{current_date}.avro"
        print(f'here is file_name = {file_name}')
        bytes_io = BytesIO()
        bytes_io.seek(0)
        fastavro.writer(bytes_io, self.get_avro_schema(), json_list)
        bytes_io.seek(0)
        self.repo_s3.client.upload_fileobj(bytes_io, METADATA_BUCKET_NAME, file_name)
"""
