from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Track(models.Model):
    title = models.CharField(max_length=250)
    artist = models.CharField(max_length=250)
    duration = models.FloatField()
    last_play = models.DateTimeField()
