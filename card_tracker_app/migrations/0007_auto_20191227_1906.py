# Generated by Django 2.2.7 on 2019-12-27 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card_tracker_app', '0006_auto_20191226_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set',
            name='series',
        ),
        migrations.DeleteModel(
            name='Series',
        ),
    ]
