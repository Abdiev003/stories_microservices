from flask import render_template
from .config.celery import celery
from .models import Subscriber

from .cache import ReadCache
from .publisher import Publish


@celery.task(name='send_mail_to_subscribers')
def send_mail_to_subscribers():
    cache = ReadCache()
    post_list = cache.load_data()
    html = render_template('subscribers/subscriber_mail.html', post_list=post_list)
    subject = 'Last Stories'
    to = [email.email for email in Subscriber.query.filter_by(is_active=True)]
    event_type = 'send_mail'
    data = {
        'subject': subject,
        'body': html,
        'to': to,
    }
    Publish(data=data, event_type=event_type)
