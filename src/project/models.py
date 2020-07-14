from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.urls import reverse
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


class Project(DesignBaseClass):
    """
        Project Models 
    """

    access_token = models.UUIDField(default=uuid.uuid4)

    description = models.TextField(max_length=512)

    image = models.ImageField(default='project_header/default.png',
                              upload_to='project_header', blank=True, null=True)
    logo = models.ImageField(default='project_logo/default.png',
                             upload_to='project_logo', blank=True, null=True)

    password = models.CharField(
        max_length=255, default='', blank=True, null=True)
    logo_thumbnail = ImageSpecField(source='logo',
                                    processors=[ResizeToFill(150, 150)],
                                    format='JPEG',
                                    options={'quality': 60})

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.id})


class Team(DesignBaseClass):
    """
    Teams for Capstone Project (Profanity Check)
    """
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, default=None, blank=True, null=True)
    description = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    token = models.UUIDField(
        default=uuid.uuid4)  # email joining
    password = models.CharField(
        max_length=255, default='', blank=True, null=True)

    def get_absolute_url(self):
        return reverse("team-detail", kwargs={"pk": self.pk})

    # project_admin = models.ForeignKey(
    #     User, on_delete=models.PROTECT, default=None, blank=True, null=True)

    # def checkMembers(self):
    #     """
    #     Query to check wether there are less than 2 members on the group
    #     """
    #     if (1):
    #         return True
    #     else:
    #         return ValidationError(" Less 2 Members not Allowed")
