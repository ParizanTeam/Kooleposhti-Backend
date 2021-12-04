from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kooleposhti.settings')

app = Celery('Kooleposhti')

app.autodiscover_tasks()
