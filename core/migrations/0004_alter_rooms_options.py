# Generated by Django 5.2.3 on 2025-06-28 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rooms'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rooms',
            options={'ordering': ['-updated', '-created'], 'verbose_name_plural': 'Rooms'},
        ),
    ]
