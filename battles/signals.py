from django.db.models.signals import post_save
from django.dispatch import receiver

from battles import models


@receiver(post_save, sender=models.Battle)
def create_hashtags(sender, **kwargs):
    hashtags = [kwargs['instance'].hashtag_1_name,
                kwargs['instance'].hashtag_2_name]

    for hastag in hashtags:
        obj, created = models.Hashtag.objects.get_or_create(name=hastag)
