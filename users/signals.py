from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .services import UserFolderService


@receiver(post_save, sender=User)
def create_user_folder(sender, instance, created, **kwargs):
    if created:
        service = UserFolderService()
        service.create_user_folder(instance.username)
