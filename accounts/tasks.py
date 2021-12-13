from celery import shared_task
from django.contrib.auth import get_user_model

from accounts.api.utils import send_email

User = get_user_model()


@shared_task
def send_email_task(user_id, email_type, new_email=False):
    user = User.objects.get(id=user_id)
    send_email(user, email_type, new_email)
