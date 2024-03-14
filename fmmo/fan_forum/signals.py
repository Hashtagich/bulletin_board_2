from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Author, User
from .models import PostCategory
from .tasks import send_notifications



@receiver(post_save, sender=User)
def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)


# Связываем функцию create_author с сигналом post_save
post_save.connect(create_author, sender=User)


@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subs = []
        for i in categories:
            subs += i.subscriber.all()

        subs_mail = [sub.email for sub in subs]

        send_notifications.delay(
            preview=instance.preview(),
            pk=instance.pk,
            title=instance.title,
            sub_list=subs_mail,
        )
