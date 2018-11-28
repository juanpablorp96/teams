from django.utils import timezone
from django.db import models
from django.conf import settings
import django


class Team(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, null=True)
    create_date = models.DateField(default=django.utils.timezone.now)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name
