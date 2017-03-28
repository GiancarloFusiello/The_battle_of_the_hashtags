from django.db.models.signals import post_save
from django.dispatch import receiver

from battles import models
from battles.tasks import battle


@receiver(post_save, sender=models.Battle)
def create_hashtags(sender, **kwargs):
    battle(kwargs['instance'].id)
