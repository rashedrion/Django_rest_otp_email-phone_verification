from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import uuid
from django.conf import settings


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)

    email_verification_token = models.CharField(
        max_length=100, null=True, blank=True)
    forget_password_token = models.CharField(
        max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def name(self):
        return self.first_name+' '+self.last_name

    def __str__(self):
        return self.email


@receiver(post_save, sender=User)
def sent_email_token(sender, instance, created,  **kwargs):
    if created:

        try:

            subject = "your email need to be verified"
            message = f'hi click on the link to verifiy email{uuid.uuid4()}'
            email_from = settings.EMAIL_HOST_USER
            recipent_list = [instance.email]
            send_mail(subject, message, email_from, recipent_list)

        except Exception as e:
            print(e)
