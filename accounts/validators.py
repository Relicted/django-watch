from registration import validators
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

CUSTOM_RESERVED_NAMES = [
    '',
]

VALIDATORS = validators.DEFAULT_RESERVED_NAMES + CUSTOM_RESERVED_NAMES

class UserRegValid(object):
    """
    CHECK USER EMAIL AND USERNAME. CREATE ERROR IF EXISTS
    """
    def __init__(self, name, email):
        self.TAKEN = _('Username is already taken')
        self.BAD_CHAR = _('CHANGE SYMBOLS ERROR')
        self.RESERVED = _("Sorry, name '{}' is a reserved word").format(name)
        self.ERROR = {}
        self.username_invalid(name)
        self.email_invalid(email)

    def username_invalid(self, name):
        if name in VALIDATORS:
            self.ERROR['username'] = self.RESERVED
        elif User.objects.filter(username__iexact=name).exists():
            self.ERROR['username'] = self.TAKEN

    def email_invalid(self, email):
        if User.objects.filter(email__iexact=email).exists():
            self.ERROR['email'] = _("Email is already taken")