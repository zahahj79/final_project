from django.db import models


class Data(models.Model):
    # humidity=models.CharField(max_length=10)
    temperature = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    location = models.CharField(max_length=30, default='--')
