from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username, is_active=True)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user