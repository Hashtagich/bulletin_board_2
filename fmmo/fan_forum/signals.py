from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Author, User


@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)


# Связываем функцию create_author с сигналом post_save
post_save.connect(create_author, sender=User)