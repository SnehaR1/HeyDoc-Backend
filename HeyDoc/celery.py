from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HeyDoc.settings")
app = Celery("HeyDoc")


app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    broker_connection_retry=settings.CELERY_BROKER_CONNECTION_RETRY,
    broker_connection_retry_on_startup=settings.CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP,
)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
