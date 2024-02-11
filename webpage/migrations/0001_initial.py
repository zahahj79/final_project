# Generated by Django 4.2.6 on 2023-10-28 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timetemp', models.DateTimeField()),
                ('temp', models.FloatField()),
                ('hum', models.FloatField()),
            ],
        ),
    ]
