# Generated by Django 4.2.6 on 2023-12-03 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0003_data_delete_sensordata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='humidity',
        ),
    ]
