from dataclasses import dataclass


@dataclass
class UnsplashModel:
    count_of_images: int
    query: str
