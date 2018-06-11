from celery import Celery
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weatherapp.settings")

import django
django.setup()

app = Celery('weatherapp', broker='amqp://localhost', backend='amqp://localhost')
