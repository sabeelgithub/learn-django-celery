from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from decouple import config

from celery.schedules import crontab
from datetime import timedelta

REDIS_BROKER_URL = config('REDIS_BROKER_URL')

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery.settings')

# Create a Celery instance.
app = Celery('django_celery')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')

# Load any custom config from Django settings.
app.config_from_object(settings, namespace='CELERY')

app.conf.broker_transport_options = {
    # No SSL options needed
}

app.conf.broker_connection_retry_on_startup = True
app.conf.worker_cancel_long_running_tasks_on_connection_loss = True

app.conf.broker_url = REDIS_BROKER_URL
app.conf.accept_content = ['json']
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json' 
app.conf.timezone = 'Asia/Kolkata'
app.conf.result_backend = REDIS_BROKER_URL
# app.conf.result_backend = 'django-db'

# Autodiscover tasks from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# app.conf.beat_schedule = {
#     'delete-old-locations-every-24-hours': {
#         'task': 'test.tasks.delete_old_locations',  # Adjust to your app's name
#         'schedule': crontab(hour=0, minute=0),  # Every day at midnight (24 hours)
#     },
# }
app.conf.beat_schedule = {
    'delete-old-locations-every-30-seconds': {
        'task': 'test.tasks.delete_old_locations',  # Adjust to your app's name
        'schedule': timedelta(seconds=30),  # Run every 30 seconds
    },
}

