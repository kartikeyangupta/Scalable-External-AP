import os
from celery import Celery
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pdf_reader.settings')

app = Celery('pdf_reader')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
