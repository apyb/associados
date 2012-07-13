from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

NEW_USERNAME_LENGTH = 255  # Max length for MySQL

def monkey_patch_username():
    username = User._meta.get_field("username")
    username.max_length = NEW_USERNAME_LENGTH
    for v in username.validators:
        if isinstance(v, MaxLengthValidator):
            v.limit_value = NEW_USERNAME_LENGTH

monkey_patch_username()
