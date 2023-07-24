from typing import List

import requests
import json

from allmemes.amazon.storage.s3 import S3
from allmemes.models.image_model import ImageModel
from models.unsplash_model import UnsplashModel
from unsplash_controller import UNSPLASH_ACCESS_KEY, UNSPLASH_SOURCE, UNSPLASH_URL


class UnsplashController:
    def __init__(self, unsplash_model: UnsplashModel):
        self.unsplash_model = unsplash_model
        self.s3 = S3()

    def download_pictures(self) -> bool:
        list_of_images = self._get_list_of_pictures()
        self.s3.upload_memes(list_of_images)
        self.s3.upload_metadata(list_of_images)
        return True

    def _get_list_of_pictures(self) -> List[ImageModel]:

        # получаем данные из Unsplash API
        response = requests.get(UNSPLASH_URL, params={
            'query': self.unsplash_model.query,
            'page': 1,
            'per_page': self.unsplash_model.count_of_images,
            'client_id': UNSPLASH_ACCESS_KEY
        })

        # преобразуем ответ в формат json
        data = json.loads(response.text)
        print(f'here is data = {data}')
        # проходим по всем изображениям и скачиваем их на компьютер
        list_of_images = []
        for image in data['results']:
            print(f'here is image = {image}')
            image_url = image['urls']['raw']
            file_name = ImageModel.get_name(source=UNSPLASH_SOURCE, sub_source=self.unsplash_model.query,
                                            photo_prefix=ImageModel.photo_prefix())
            list_of_images.append(
                ImageModel(
                    url=image_url,
                    source=UNSPLASH_SOURCE,
                    sub_source=self.unsplash_model.query,
                    caption='mock',
                    file_name=file_name
                )
            )
        return list_of_images



