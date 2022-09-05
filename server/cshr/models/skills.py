""" database office model """
from django.db import models


class Skills(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
