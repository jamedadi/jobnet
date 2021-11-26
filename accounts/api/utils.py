from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


def create_activation_link(user):
    confirmation_token = default_token_generator.make_token(user)
    return f'{settings.ACTIVATION_LINK_URL}?user_id={user.id}&confirmation_token={confirmation_token}'


def send_verification_email(user):
    user.send_email(
        subject='Jobnet : verify your email',
        message=create_activation_link(user)
    )
