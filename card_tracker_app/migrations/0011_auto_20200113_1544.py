# Generated by Django 3.0 on 2020-01-13 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card_tracker_app', '0010_cardowned'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cardowned',
            table='card_tracker_app_card_owned',
        ),
    ]
