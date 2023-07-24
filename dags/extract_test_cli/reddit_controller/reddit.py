from typing import List

from allmemes.amazon.storage.s3 import S3
from allmemes.models.image_model import ImageModel
from models.reddit_model import RedditModel
from reddit_controller import REDDIT_SOURCE
from reddit_controller.reddit_client import RedditClient


class RedditController:
    def __init__(self, reddit_model: RedditModel):
        self.reddit_client = RedditClient()
        self.reddit_model = reddit_model
        self.s3 = S3()

    def download_pictures(self) -> bool:
        list_of_images = self._get_list_of_pictures()
        self.s3.upload_memes(list_of_images)
        self.s3.upload_metadata(list_of_images)
        return True

    def _get_list_of_pictures(self) -> List[ImageModel]:
        result_list = []
        line = self.reddit_model.list_of_subreddits
        print(f'here is line = {line}')
        sub = line.strip()
        print(f"HERE IS sub = {sub}")
        subreddit = self.reddit_client.reddit.subreddit(sub)
        print(f"Now we working with {subreddit} subreddit")
        for submission in subreddit.new(limit=self.reddit_model.count_of_images):
            if "jpg" in submission.url.lower() or "png" in submission.url.lower():
                file_name = ImageModel.get_name(source=REDDIT_SOURCE, sub_source=line, photo_prefix=ImageModel.photo_prefix())
                result_list.append(
                    ImageModel(
                        url=submission.url.lower(),
                        source=REDDIT_SOURCE,
                        sub_source=line,
                        caption=submission.title,
                        file_name=file_name
                    )
                )
        return result_list
