# Generated by Django 2.1 on 2018-09-27 00:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PostModel',
            new_name='Post',
        ),
    ]
