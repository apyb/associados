from django.db import migrations
from django.contrib.auth import get_user_model


def reset_all_passwords(apps, schema_editor):
    User = get_user_model()
    users = User.objects.all()

    for user in users:
        new_random_password = User.objects.make_random_password(length=40)
        user.set_password(new_random_password)
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0010_sort_members_by_name'),
    ]

    operations = [
        migrations.RunPython(reset_all_passwords),
    ]
