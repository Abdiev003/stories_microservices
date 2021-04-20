import json

from .config.extensions import RedisConfig


class Publish(RedisConfig):

    def __init__(self, data, event_type):
        self.data = {
            'data': data,
            'event_type': event_type
        }
        self.publish_data()

    def stringify(self):
        return json.dumps(self.data)

    def publish_data(self):
        self.client().publish(self.CHANNEL_NAME, self.stringify())
