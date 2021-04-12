from django.db import models
from ProjectControl.models import Project


def upload_back(instance, filename):
    return f"static\\themes-static\\{instance.name}\\back.{filename[filename.rfind('.') + 1:]}"


def upload_small(instance, filename):
    return f"static\\themes-static\\{instance.name}\\small.{filename[filename.rfind('.') + 1:]}"


# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    projects = models.ManyToManyField(Project, related_name="theme", blank=True)
    background = models.ImageField(upload_to=upload_back, blank=True, null=True)
    background_small = models.ImageField(upload_to=upload_small, default="static\\images\\no-image.png")


    def __str__(self):
        return f"{self.name}"
