# Generated by Django 5.2.3 on 2025-07-07 23:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myteam', '0005_teamtasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamtasks',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myteam.teams'),
        ),
    ]
