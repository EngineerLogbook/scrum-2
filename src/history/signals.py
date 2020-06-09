from django.db.models.signals import post_save
from django.contrib.auth.models import User
from project.models import Project, Team
from log.models import Logger
from django.dispatch import receiver
from .models import History


@receiver(post_save, sender=Logger)
def create_profile(sender, instance, created, **kwargs):
    # if created:
    History.objects.create(
        user=instance.user,
        logger=instance,
        project=instance.project,
        team=instance.project.team,
        message=f'{instance.title} created'
    )
    # else:
    #     History.objects.create(
    #         user=instance.user,
    #         logger=instance,
    #         project=instance.project,
    #         team=instance.project.team,
    #         message=f'{instance.title} Updated '
    #     )
