import redis
import json
from .config import RedisConfig
from .mail import SendMail


class Handler:
    event_type = 'send_mail'

    def __init__(self, message):
        if message.get("type") == "message":
            self.data = self.load_data(message)
            if self.check_event_type():
                self.send_mail()

    def check_event_type(self):
        if self.data['event_type'] == self.event_type:
            return True
        return False

    def load_data(self, message):
        data = message.get('data')
        return json.loads(data)

    def get_mail_data(self):
        mail_data = self.data.get('data')
        return {
            'body': mail_data.get('body'),
            'to': mail_data.get('to'),
            'subject': mail_data.get('subject'),
        }

    def send_mail(self):
        mail_data = self.get_mail_data()
        SendMail(**mail_data)

def subscribe():
    redis_conn = RedisConfig.client()
    p = redis_conn.pubsub()
    p.subscribe(**{RedisConfig.CHANNEL_NAME: Handler})
    thread = p.run_in_thread()
