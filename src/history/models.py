from django.db import models
import uuid
from django.contrib.auth.models import User
from log.models import Logger
from project.models import Project, Team
# Create your models here.


class History(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, null=True, blank=True)
    logger = models.ForeignKey(Logger, on_delete=models.PROTECT, null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.message}'
