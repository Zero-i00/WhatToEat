import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WhatToEatToday.settings')
app = Celery('WhatToEatToday')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(related_name='tasks', packages=['scrapers'])
app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')