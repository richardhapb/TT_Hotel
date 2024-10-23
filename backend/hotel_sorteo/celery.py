from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_sorteo.settings')
app = Celery('hotel_sorteo')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
