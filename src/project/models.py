from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# Create your models here.


class DesignBaseClass(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=127)
    slug = models.SlugField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=True)
    reviewed = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        # Slugify the name for the URL
        self.slug = slugify(self.title)
        super(DesignBaseClass, self).save(*args, **kwargs)

    def publishedFlip(self, *args, **kwargs):
        """
        Published Flip Switch
        """
        self.published = not self.published
        try:
            self.save(*args, **kwargs)
        except:
            ValidationError("Internal Server Error")

    def reviewFlip(self, *args, **kwargs):
        """
        Published revied Flip
        """
        self.reviewed = not self.reviewed
        try:
            self.save(*args, **kwargs)
        except:
            ValidationError("Internal Server Error")


class Team(DesignBaseClass):
    """
    Teams for Capstone Project Profanity Check
    """
    description = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    token = models.UUIDField(
        default=uuid.uuid4)  # email joining

    def checkMembers(self):
        """
        Query to check wether there are less than 2 members on the group
        """
        if (1):
            return True
        else:
            return ValidationError(" Less 2 Members not Allowed")


class Project(DesignBaseClass):
    """
        Project Models 
    """

    team = models.ForeignKey(
        Team,  on_delete=models.PROTECT)
    access_token = models.UUIDField(
        default=uuid.uuid4)

    description = models.TextField(max_length=512)

    image = models.ImageField(
        upload_to='project_header', blank=True, null=True)
    logo = models.ImageField(upload_to='project_logo', blank=True, null=True)
