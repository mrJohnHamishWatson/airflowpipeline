import click

from flickr_controller.flickr import FlickrController
from models.flickr_model import FlickrModel
from models.reddit_model import RedditModel
from models.unsplash_model import UnsplashModel
from reddit_controller.reddit import RedditController
from unsplash_controller.unsplash import UnsplashController


@click.group()
def cli():
    pass


@cli.command(name="get_reddit")
@click.argument("count_of_image", required=True, type=click.INT)
@click.argument("subreddits", required=True, type=click.STRING)
def get_reddit(count_of_image: int, subreddits: str):
    reddit_model = RedditModel(
        count_of_images=count_of_image,
        list_of_subreddits=subreddits,
    )
    print(f"Here is reddit_model = {reddit_model}")
    print(f"here is count_of_image = {reddit_model.count_of_images}")
    print(f'here is subreddits = {reddit_model.list_of_subreddits}')
    reddit_controller = RedditController(reddit_model)
    if reddit_controller.download_pictures():
        print("Everything is ok")

    return True


@cli.command(name="get_unsplash")
@click.argument("count_of_image", required=True, type=click.INT)
@click.argument("tag", required=True, type=click.STRING)
def get_unsplash(count_of_image: int, tag: str):
    unsplash_model = UnsplashModel(
        count_of_images=count_of_image,
        query=tag,
    )
    unsplash_controller = UnsplashController(unsplash_model)
    if unsplash_controller.download_pictures():
        print("Everything is ok")

    return True


@cli.command(name="get_flickr")
@click.argument("count_of_image", required=True, type=click.INT)
@click.argument("tag", required=True, type=click.STRING)
def get_flickr(count_of_image: int, tag: str):
    flickr_model = FlickrModel(count_of_images=count_of_image,
                               tag=tag)
    print(f'here is flickr_model = {flickr_model}')
    flickr_controller = FlickrController(flickr_model)
    if flickr_controller.download_pictures():
        print(f"Images for tag {tag} in count of {count_of_image} was downloaded to s3")


def main():
    cli()


if __name__ == '__main__':
    main()
