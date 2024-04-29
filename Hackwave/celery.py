from __future__ import absolute_import, unicode_literals
from celery import Celery

# This is the name of your project
app = Celery('Hackwave')

app.config_from_object('django.conf:settings', namespace='CELERY')

# This line will auto discover tasks in your Django project.
app.autodiscover_tasks()