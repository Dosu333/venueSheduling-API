from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault('DJANGO_SETINGS_MODULE', 'venApi.settings')

app = Celery('venApi')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'delete-every-minute': {
#         'task': 'tasks.add',
#         'schedule': crontab(),
#     },
# }

@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')