# Generated by Django 4.2.6 on 2023-12-06 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0005_data_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='location',
            field=models.CharField(default='--', max_length=30),
        ),
    ]