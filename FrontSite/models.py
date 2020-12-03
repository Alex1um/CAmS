from django.db import models
import os
from markdown import markdown
from django.contrib.auth.models import User
# Create your models here.

#
# class User(models.Model):
#     NickName = models.CharField(max_length=30)
#     # TODO: Make table for it
#     ClientType = models.CharField(
#         choices=[("github", "Registered with GitHub"), ("local",
#                                                         "Registered on the site")],
#         max_length=255)
#
#     def __str__(self):
#         return f"{self.id} - {self.NickName}"


class Projects(models.Model):
    Name = models.CharField(max_length=100)
    Creator = models.ForeignKey(User, models.PROTECT)
    Owners = models.ManyToManyField(User,
                                    related_name="owners")
    AllowedUsers = models.ManyToManyField(User,
                                          related_name='permitted',
                                          blank=True)
    Parents = models.ManyToManyField("self",
                                     related_name="dependent",
                                     blank=True,
                                     symmetrical=False,
                                     through='Dependence',
                                     )
    Home_markdown = models.TextField(blank=True, default=None, null=True)
    Home_html = models.TextField(null=True, blank=True, default=None)
    Relations = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.id} - {self.Name} by {{{self.Creator}}}"

    def save(self, *args, **kwargs):
        if self.Home_markdown:
            self.Home_html = markdown(self.Home_markdown)
        super().save(*args, **kwargs)
        # os.mkdir(f"..\\Projects\\{self.id}")


class Dependence(models.Model):
    Dependence = models.ForeignKey(Projects,
                                   on_delete=models.DO_NOTHING,
                                   related_name='dependencies',
                                   null=False,
                                   default=1)
    Parent = models.ForeignKey(Projects,
                               on_delete=models.DO_NOTHING,
                               related_name='parent',
                               null=False)

    Status = models.CharField(choices=(("warning", "Out of date"),
                                       ("success", "Up to date"),
                                       ("danger", "Edited")), max_length=10,
                              default="danger")
    # UsedVersion = models.CharField()