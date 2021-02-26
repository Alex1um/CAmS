from django.contrib.auth.models import User
from django.db import models
from markdown2 import markdown
import json


# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(
        User,
        models.PROTECT, related_name="created_projects"
    )
    owners = models.ManyToManyField(
        User,
        related_name="owner_of_projects"
    )
    allowed_users = models.ManyToManyField(
        User,
        related_name='allowed_projects',
        blank=True
    )
    home_markdown = models.TextField(blank=True, default=None, null=True)
    home_html = models.TextField(null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=200)
    version = models.CharField(max_length=30, default="0.1.0")
    short_description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.id} - {self.name} by {{{self.creator}}}"

    def save(self, *args, **kwargs):
        if self.home_markdown:
            self.home_html = markdown(self.home_markdown)
        files = [{
            "type": "dir",
            "name": self.name,
            "files": [],
        }]
        super().save(*args, **kwargs)
        create_files(self, files, self.version)
        # os.mkdir(f"..\\projects\\{self.id}")


class FileDirectory(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="files",
    )
    files = models.JSONField(null=True, blank=True, default=None)
    version = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.project}({self.version})"


def create_files(proj: Project, files, version):
    return FileDirectory.objects.create(project=proj,
                                        files=files,
                                        version=version)


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
    files = models.ForeignKey(
        FileDirectory,
        on_delete=models.CASCADE,

    )

    def __str__(self):
        return f"{self.project}({self.files.version}) -> {self.project_dependency}"


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