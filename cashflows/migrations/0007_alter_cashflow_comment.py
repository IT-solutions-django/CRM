# Generated by Django 5.1.4 on 2025-01-10 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashflows', '0006_alter_cashflow_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashflow',
            name='comment',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Комментарий'),
        ),
    ]
