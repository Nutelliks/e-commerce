from celery import shared_task
from .models import User

import logging

user_logger = logging.getLogger(__name__)


@shared_task
def send_welcome_email(user_id):
    try:
        user = User.objects.get(id=user_id)
        user_logger.info(f"Would send welcome email to user {user.email} (id={user.id})")
    except User.DoesNotExist:
        user_logger.error(f"User with id={user_id} does not exist")