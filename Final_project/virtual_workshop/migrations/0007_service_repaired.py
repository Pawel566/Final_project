# Generated by Django 5.0.3 on 2024-04-08 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_workshop', '0006_remove_service_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='repaired',
            field=models.BooleanField(default=False, verbose_name='Naprawione'),
        ),
    ]