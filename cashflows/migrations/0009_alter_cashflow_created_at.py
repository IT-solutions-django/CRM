# Generated by Django 5.1.4 on 2025-01-13 09:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflows', '0008_alter_cashflow_options_remove_cashflow_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashflow',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата'),
        ),
    ]
