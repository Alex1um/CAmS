from django.contrib.auth.models import User
from django.db import models
from markdown2 import markdown
import json


# Create your models here.
import uuid


class Project(models.Model):
    name = models.CharField(max_length=100)
    creation_date = models.DateTimeField()
    creator = models.ForeignKey(
        User,
        models.PROTECT,
        related_name="created_projects",
    )
    owners = models.ManyToManyField(
        User,
        related_name="owner_of_projects",
    )
    allowed_users = models.ManyToManyField(
        User,
        related_name='allowed_projects',
        blank=True
    )

    def __str__(self):
        return f"{self.id} - {self.name} by {{{self.creator}}}"


class Version(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="versions",
    )
    files = models.JSONField(null=True, blank=True, default=dict)
    name = models.CharField(max_length=30)
    uuid = models.UUIDField(primary_key=False,
                            editable=False,
                            default=uuid.uuid4,
                            unique=True)
    creation_date = models.DateTimeField(auto_now=True)
    home_markdown = models.TextField(blank=True, default=None, null=True)
    home_html = models.TextField(null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=200)
    short_description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.project} - {self.name} - {self.uuid}"

    def save(self, *args, **kwargs):
        if self.home_markdown:
            self.home_html = markdown(self.home_markdown)
        if not self.files:
            self.files = [{
                "type": "dir",
                "name": self.project.name,
                "files": [],
            }]
        super(Version, self).save(*args, **kwargs)


class Dependence(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.DO_NOTHING,
        related_name='dependencies'
    )
    project_dependency = models.ForeignKey(
        Project,
        on_delete=models.DO_NOTHING,
        related_name='as_dependence',
    )
    project_dependency_version = models.ForeignKey(
        Version,
        on_delete=models.DO_NOTHING,
        related_name='as_dependence'
    )
    project_versions = models.ManyToManyField(
        Version,
        "dependencies",
        blank=True,
    )

    files = models.JSONField(null=True, blank=True, default=dict)

    def __str__(self):
        return f"{self.project_dependency}({self.project_dependency_version.name}) -> {self.project}"


class ProjectManager(models.Manager):
    def create_project(
            self,
            dependent_projects: list[Dependence, str, dict] = None,
            *args,
            **kwargs
    ):
        obj = self.create(*args, **kwargs)
        files = {
            "type": "dir",
            "name": obj.name,
            "files": [],
        }
        if dependent_projects:
            for p, v, f in dependent_projects:
                Dependence.objects.create(
                    project=obj,
                    project_dependency=p,
                    project_version=v,
                    files=f,
                )