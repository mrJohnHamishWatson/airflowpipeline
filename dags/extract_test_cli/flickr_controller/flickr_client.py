import flickrapi

from flickr_controller import FLICKR_KEY, FLICKR_SECRET


class FlickrClient:
    def __init__(self):
        self.flickr = flickrapi.FlickrAPI(FLICKR_KEY, FLICKR_SECRET, cache=True)
