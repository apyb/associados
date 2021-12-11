from django.core.management import call_command
from django.db import migrations


def load_fixture(apps, schema_editor):
    call_command('loaddata', 'site_init.json', app_label='core')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        #migrations.RunPython(load_fixture)
    ]
