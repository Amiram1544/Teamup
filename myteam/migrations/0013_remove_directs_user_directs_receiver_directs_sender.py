# Generated by Django 5.2.3 on 2025-07-12 19:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myteam', '0012_directs'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directs',
            name='user',
        ),
        migrations.AddField(
            model_name='directs',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_directs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='directs',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_directs', to=settings.AUTH_USER_MODEL),
        ),
    ]
