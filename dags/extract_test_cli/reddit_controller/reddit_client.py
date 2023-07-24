import praw

from reddit_controller import CLIENT_ID_REDDIT, CLIENT_SECRET_REDDIT, USER_AGENT_REDDIT, USERNAME_REDDIT, \
    PASSWORD_REDDIT


class RedditClient:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=CLIENT_ID_REDDIT,
            client_secret=CLIENT_SECRET_REDDIT,
            user_agent=USER_AGENT_REDDIT,
            username=USERNAME_REDDIT,
            password=PASSWORD_REDDIT,
        )
