import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bi_dashboard.settings")

app = Celery("bi_dashboard")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()