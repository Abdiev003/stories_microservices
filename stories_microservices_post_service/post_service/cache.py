import json

from .config.extensions import RedisConfig


class SaveCache(RedisConfig):

    def __init__(self, new_post):
        self.data = self.dump_data(new_post)
        self.save()

    def dump_data(self, new_post):
        return json.dumps(new_post)

    def save(self):
        self.client.rpush('posts', self.data)