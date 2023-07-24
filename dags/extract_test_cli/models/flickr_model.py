from dataclasses import dataclass


@dataclass
class FlickrModel:
    count_of_images: int
    tag: str
