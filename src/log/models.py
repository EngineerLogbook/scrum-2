from django.db import models
from django.contrib.auth.models import User
import uuid
from project.models import Team, Project, DesignBaseClass
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.


class Logger(DesignBaseClass):

    note = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    date_modified = models.DateTimeField(null=True)
    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, null=True, blank=True)

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
    filetype = models.CharField(max_length=100, choices=FILE_TYPES)
    log = models.ForeignKey(Logger, on_delete=models.PROTECT, )


class LogURL(models.Model):
    url = models.URLField()
    log = models.ForeignKey(Logger,  on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.url}'
