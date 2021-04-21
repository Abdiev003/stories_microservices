import json

from .config.extensions import RedisConfig


class ReadCache(RedisConfig):

    def __init__(self):
        self.data = self.read()

    def load_data(self):
        return [json.loads(json.loads(data)) for data in self.data]

    def read(self):
        return self.client.lrange('posts', 0, -1)
