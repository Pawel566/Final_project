# Generated by Django 5.0.3 on 2024-04-10 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_workshop', '0010_jobtool_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobtool',
            name='quantity',
        ),
    ]
