from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode


def generate_token_and_user_id_base64(user):
    token = default_token_generator.make_token(user)
    user_id_base64 = urlsafe_base64_encode(smart_bytes(user.id))
    return {'uib64': user_id_base64, 'token': token}


def reset_password_link_generator(user):
    relative_link = reverse('accounts:confirm-reset-password', kwargs=generate_token_and_user_id_base64(user))
    link = 'http://127.0.0.1:8000' + relative_link
    return f'Hi {user.username} use this link to reset your password: {link}'


def email_verification_link_generator(user):
    relative_link = reverse('accounts:verify-email', kwargs=generate_token_and_user_id_base64(user))
    link = 'http://127.0.0.1:8000' + relative_link
    return f'Hi {user.username} use this link to verify your email: {link}'


def email_change_link_generator(user):
    relative_link = reverse('accounts:change-email-verify', kwargs=generate_token_and_user_id_base64(user))
    link = 'http://127.0.0.1:8000' + relative_link
    return f'Hi {user.username} use this link to change your email: {link}'


def body_generator(user, email_type):
    if email_type == 'email_verification':
        return {
            'subject': 'Job net: verify your email',
            'message': email_verification_link_generator(user)
        }
    elif email_type == 'reset_password':
        return {
            'subject': 'Job net: reset password',
            'message': reset_password_link_generator(user)
        }
    elif email_type == 'change-email':
        return {
            'subject': 'Job net: change your email',
            'message': email_change_link_generator(user)
        }


def send_email(user, email_type, new_email=False):
    user.email_user(**body_generator(user, email_type), new_email=new_email)
