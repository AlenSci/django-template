from __future__ import absolute_import, unicode_literals

import os

import environ
from celery import Celery

from spesific_app_name.settings import PROJECT_NAME

env = environ.Env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{PROJECT_NAME}.settings')
app = Celery(PROJECT_NAME)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(name="celery.ping")
def ping():
    return '================================= pong ================================='
