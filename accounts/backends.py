from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class CaseInsensitiveModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username__iexact=username) |
                Q(email__iexact=username))
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

