from django.db.models.signals import post_save
from django.contrib.auth.models import User
from project.models import Project, Team
from log.models import Logger
from django.dispatch import receiver
from .models import History

# TODO ADD PRE SAVE FUNCTIONALITY


@receiver(post_save, sender=Logger)
def log_history(sender, instance, created, **kwargs):
    if created:
        History.objects.create(
            user=instance.user if instance.user is not None else None,
            logger=instance,
            project=instance.project if instance.project is not None else None,
            team= None if (instance.project is not None) else None,
            message=f'Log "{instance.title}" Created'
        )



    else:
        History.objects.create(
            user=instance.user if instance.user is not None else None,
            logger=instance,
            project=instance.project if instance.project is not None else None,
            team= None if (instance.project is not None) else None,
            message=f'Log "{instance.title}" Modified'
        )

@receiver(post_save, sender=Project)
def project_history(sender, instance, created, **kwargs):
    if created:
        History.objects.create(
            project=instance,
            team=instance.team,
            message=f'Project "{instance.title}" Created'
        )



    else:
        History.objects.create(
            project=instance,
            team=instance.team,
            message=f'Project "{instance.title}" Modified'
        )


@receiver(post_save, sender=Team)
def team_history(sender, instance, created, **kwargs):
    if created:
        History.objects.create(
            team=instance,
            message=f'Team "{instance.title}" Created'
        )



    else:
        History.objects.create(
            team=instance,
            message=f'Team "{instance.title}" Modified'
        )
