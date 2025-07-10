from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings
from django.apps import apps

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_teacher:
            group, _ = Group.objects.get_or_create(name='Teacher')
        else:
            group, _ = Group.objects.get_or_create(name='Student')
        instance.groups.add(group)
