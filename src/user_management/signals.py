from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from .models import Profile

import threading


class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def send_email(sender, instance, created, **kwargs):
    if created:
        current_site = get_current_site(request=None)
        mail_subject = 'Activate your logbook account.'
        message = render_to_string('user_management/email/acc_active_email.html', {
            'user': instance,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': account_activation_token.make_token(instance),
        })
        to_email = instance.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        EmailThread(email).start()


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
