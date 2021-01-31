from __future__ import absolute_import

import os

from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shifu.settings')

from django.conf import settings  # noqa
from django.db import connections
from django.db.utils import OperationalError
db_conn = connections['default']
connected = False
while not connected:
	try:
	    c = db_conn.cursor()
	except OperationalError:
	    connected = False
	else:
	    connected = True

app = Celery('shifu', backend=settings.CELERY_RESULT_BACKEND, broker=settings.BROKER_URL)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
