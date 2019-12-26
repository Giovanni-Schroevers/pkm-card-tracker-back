# Generated by Django 2.2.7 on 2019-12-26 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('card_tracker_app', '0005_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='action',
            name='card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='card_action', to='card_tracker_app.Card'),
        ),
        migrations.AlterField(
            model_name='action',
            name='set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='set_action', to='card_tracker_app.Set'),
        ),
        migrations.AlterField(
            model_name='action',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_action', to=settings.AUTH_USER_MODEL),
        ),
    ]
