from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

CUSTOM_RESERVED_NAMES = [
    'host',
    'audio',
    'video',
    'settings',
    'info',
    'board',
    'contacts',
    'media',
    'profile',
    'news',
]


VALIDATORS = CUSTOM_RESERVED_NAMES

class UserRegValid(object):
    """
    CHECK USER EMAIL AND USERNAME. CREATE ERROR IF EXISTS
    """
    def __init__(self, name, email):
        self.TAKEN = _('Username is already taken')
        self.BAD_CHAR = _('Name should contain only alphanumeric symbols')
        self.RESERVED = _("Sorry, name '{}' is a reserved word").format(name)
        self.ERROR = {}
        self.username_invalid(name)
        self.email_invalid(email)

    def username_invalid(self, name):
        if name in VALIDATORS:
            self.ERROR['username'] = self.RESERVED
        elif User.objects.filter(username__iexact=name).exists():
            self.ERROR['username'] = self.TAKEN

        if not all(x.isalnum() or x.isspace() for x in name):
            self.ERROR['username'] = self.BAD_CHAR

    def email_invalid(self, email):
        if User.objects.filter(email__iexact=email).exists():
            self.ERROR['email'] = _("Email is already taken")