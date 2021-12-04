from __future__ import absolute_import, unicode_literals

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.decorators import task
# from celery. import

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    return x + y


@task(name='remove_unstaged_users_task')
def remove_unstaged_users_task():
    # celery -A Kooleposhti worker -l info
    logger.info("Removing unstaged users...")
    # return remove_unstaged_users()
