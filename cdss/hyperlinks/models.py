from django.db import models  # type: ignore

# Create your models here.


class Hyperlink(models.Model):
    name = models.SlugField(max_length=100)
    link = models.URLField(max_length=500)
    page = models.ForeignKey("pages.Page", on_delete=models.CASCADE, related_name="hyperlinks")
