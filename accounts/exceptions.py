from rest_framework.exceptions import NotAuthenticated
from django.utils.translation import gettext_lazy as _


class EmailNotVerified(NotAuthenticated):
    default_detail = _('The email of your account has not been verified yet, an activation link has been sent again')
    default_code = 'email_not_verified'
