# Generated by Django 2.2.6 on 2020-01-23 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scprojects', '0004_auto_20200123_0453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='department',
        ),
    ]
