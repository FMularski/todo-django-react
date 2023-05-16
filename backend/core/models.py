from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
