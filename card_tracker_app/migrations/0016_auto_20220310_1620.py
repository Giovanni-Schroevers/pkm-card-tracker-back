# Generated by Django 2.2.13 on 2022-03-10 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_tracker_app', '0015_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='code',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
