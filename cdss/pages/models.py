from django.db import models

# Create your models here.


class Page(models.Model):
    name = models.SlugField(max_length=100, unique=True)
    term = models.CharField(max_length=500, null=True, blank=True, default=None)
    displaytext = models.CharField(max_length=500)
    version = models.CharField(max_length=50)
    contents = models.JSONField()
