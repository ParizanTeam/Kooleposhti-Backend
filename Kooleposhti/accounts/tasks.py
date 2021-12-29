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
    # flower -A core --port=5555
    logger.info("Removing unstaged users...")
    # return remove_unstaged_users()
    # python manage.py makemigrations
    # python manage.py migrate
    # celery -A core beat -l INFo
    # celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
