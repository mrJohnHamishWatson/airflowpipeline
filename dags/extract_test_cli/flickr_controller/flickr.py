from typing import List


from allmemes.amazon.storage.s3 import S3
from allmemes.models.image_model import ImageModel
from flickr_controller.flickr_client import FlickrClient
from models import FLICKR_SOURCE
from models.flickr_model import FlickrModel


class FlickrController:
    def __init__(self, flickr_model: FlickrModel):
        self.flickr_model = flickr_model
        self.flickr_client = FlickrClient()
        self.s3 = S3()

    def download_pictures(self) -> bool:
        list_of_images = self._get_list_of_pictures()
        print(f'here is list_of_images = {list_of_images}')
        self.s3.upload_memes(list_of_images)
        self.s3.upload_metadata(list_of_images)
        return True

    def _get_list_of_pictures(self) -> List[ImageModel]:
        photos = self.flickr_client.flickr.walk(text=self.flickr_model.tag,
                                                tag_mode='all',
                                                tags=self.flickr_model.tag,
                                                extras='url_c',
                                                per_page=self.flickr_model.count_of_images,
                                                sort='relevance',
                                                )
        list_of_images = []
        c = 0
        for photo in photos:
            image_url = photo.get('url_c')
            file_name = ImageModel.get_name(source=FLICKR_SOURCE, sub_source=self.flickr_model.tag,
                                            photo_prefix=ImageModel.photo_prefix())
            list_of_images.append(
                ImageModel(
                    url=image_url,
                    source=FLICKR_SOURCE,
                    sub_source=self.flickr_model.tag,
                    caption='mock',
                    file_name=file_name
                )
            )
            c += 1
            if c == self.flickr_model.count_of_images:  # I dont know how to make it more g
                break
        return list_of_images

