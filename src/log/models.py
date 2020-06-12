from django.db import models
from django.contrib.auth.models import User
import uuid
from project.models import Team, Project, DesignBaseClass
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.


class Tags(DesignBaseClass):
    pass


class Logger(DesignBaseClass):

    note = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    date_modified = models.DateTimeField(null=True)
    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, null=True, blank=True)
    short_description = models.CharField(max_length=255, null=True, blank=True)
    tag = models.ManyToManyField(Tags, blank=True)
    default_password = models.BooleanField(default=True,)
    password = models.CharField(max_length=100, null=True, blank=True)
    access = models.ManyToManyField(
        User, related_name='user_access', related_query_name='user_access')

    def __str__(self):
        return f'{self.user.username} : {self.title}'

    def save(self, *args, **kwargs):
        # Slugify the name for the URL
        self.date_modified = timezone.now()
        super(Logger, self).save(*args, **kwargs)


class LogFile(DesignBaseClass):
    FILE_TYPES = [
        ("image", "image"),
        ("pdf", "pdf"),
        ("dwg", "dwg"),
        ("misc", "misc")
    ]

    file = models.FileField(upload_to="logfile")
    filetype = models.CharField(max_length=100, choices=FILE_TYPES, null=True, blank=True)
    log = models.ForeignKey(Logger, on_delete=models.PROTECT, null=True, blank=True)


class LogURL(models.Model):
    url = models.URLField()
    log = models.ForeignKey(Logger,  on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.url}'
