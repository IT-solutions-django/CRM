# Generated by Django 5.1.4 on 2025-01-14 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hr_candidate',
            old_name='request_datetime',
            new_name='requested_datetime',
        ),
    ]
