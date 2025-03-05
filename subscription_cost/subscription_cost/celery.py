# coding=utf-8
"""
This file contains Implementation of Celery App object for the Paymob Accept project.

Helpful links:
    - https://docs.celeryq.dev/en/v5.2.1/django/first-steps-with-django.html
"""

from __future__ import absolute_import

import os

from celery import Celery
from subscriptions.celery_config import SubscriptionCeleryConfig

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subscription_cost.settings")

app = Celery("tasks")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
# Celery will automatically discover tasks from all of your installed apps, following the tasks.py convention.
app.autodiscover_tasks()

# manually setup The periodic task schedule used by beat.
# https://docs.celeryq.dev/en/v5.2.1/userguide/periodic-tasks.html
# https://docs.celeryq.dev/en/v5.2.1/userguide/configuration.html#task-create-missing-queues
app.conf.task_create_missing_queues = True

# https://docs.celeryq.dev/en/v5.2.1/userguide/configuration.html#task-default-queue
# This queue must be listed in CELERY_QUEUES. If CELERY_QUEUES is not specified then it is automatically created
# containing one queue entry, where this name is used as the name of that queue.
app.conf.task_default_queue = "subscription-celery"

# https://docs.celeryq.dev/en/v5.2.1/userguide/configuration.html#task-queues


app.conf.task_routes = {}

app.conf.task_routes.update(SubscriptionCeleryConfig.task_routes())


