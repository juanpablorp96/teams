from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import django
from team.models import Team


class Board(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    create_date = models.DateField(default=django.utils.timezone.now)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name


class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    create_date = models.DateField(default=django.utils.timezone.now)

    def __str__(self):
        return "{}-{}".format(self.board.name, self.name)


class Task(models.Model):
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=280)
    create_date = models.DateField(default=django.utils.timezone.now)
    in_charge = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=User)

    def __str__(self):
        return "{}-{}-{}".format(self.column.board.name, self.column.name, self.title)

