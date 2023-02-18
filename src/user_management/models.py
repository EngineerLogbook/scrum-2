from django.db import models
from project.models import DesignBaseClass
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image
import uuid
# Create your models here.


class FieldStudy(DesignBaseClass):
    pass


class TechSkill(DesignBaseClass):
    pass


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    # META DATA
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Transgender', 'Transgender'),
        ('NIL', 'Prefer Not Say')
    ]
    gender = models.CharField(
        max_length=11, choices=GENDER, null=True)
    bio = models.CharField(max_length=5000, null=True, blank=True)

    # Education
    DEGREES = [
        ('Bachelors', 'Bachelors'),
        ('Master', 'Master'),
        ('Phd', 'Phd'),
    ]
    degree = models.CharField(max_length=20, choices=DEGREES, null=True)
    is_prof = models.BooleanField(default=False)
    field_study = models.ForeignKey(
        FieldStudy, on_delete=models.PROTECT, null=True, blank=True)
    YEAR = [
        (2020, 2020),
        (2021, 2021),
        (2022, 2022),
        (2023, 2023),
        (2024, 2024),
        (2025, 2025),
    ]
    year_grad = models.PositiveIntegerField(choices=YEAR, null=True)

    # Experience
    techskill = models.ManyToManyField(TechSkill, blank=True)
    # Email Verficaton
    token = models.UUIDField(default=uuid.uuid4)
    phone = models.CharField(max_length=10, null=True, blank=True)
    published = models.BooleanField(default=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}\'s Profile'

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    name = models.CharField(max_length=255, null=True)
    profile = models.ForeignKey(Profile,  on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.url}'


def validate_image(image):
    file_size = image.file.size
    limit = 2 * 1024 * 1024
    if file_size > limit:
        raise ValidationError("Max size of file is 2 MB")


class Phase(models.Model):
    name = models.CharField(max_length=255)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ("-order",)

    def __str__(self):
        return self.name


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team_member',
                              validators=[validate_image])
    linkdinURL = models.URLField()
    team = models.ManyToManyField(Phase, blank=True)
    order = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ("order",)

    def __str__(self):
        return self.name
