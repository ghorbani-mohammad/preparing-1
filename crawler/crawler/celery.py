from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTING_MODULE", "crawler.settings")
app = Celery("crawler")
app.config_from_object("django.conf.settings")
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)