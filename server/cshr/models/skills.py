""" database office model """
from django.db import models


class Skills(models.Model):
    name = models.CharField(max_length=50)
