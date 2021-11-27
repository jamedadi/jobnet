from celery import shared_task
from django.contrib.auth import get_user_model

from accounts.api.utils import send_verification_email

User = get_user_model()


@shared_task
def send_verification_email_task(user_id):
    user = User.objects.get(id=user_id)
    send_verification_email(user)
