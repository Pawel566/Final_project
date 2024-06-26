# Generated by Django 5.0.3 on 2024-04-08 12:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_workshop', '0004_jobs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fault_description', models.TextField(verbose_name='Opis usterki')),
                ('expected_pickup_date', models.DateField(verbose_name='Przewidywany czas odbioru')),
                ('model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='services_model', to='virtual_workshop.tools', verbose_name='Model narzędzia')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services_tool', to='virtual_workshop.tools', verbose_name='Narzędzie')),
            ],
        ),
    ]
