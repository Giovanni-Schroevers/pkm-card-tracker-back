# Generated by Django 2.2.7 on 2019-12-27 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card_tracker_app', '0007_auto_20191227_1906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='set',
        ),
    ]
