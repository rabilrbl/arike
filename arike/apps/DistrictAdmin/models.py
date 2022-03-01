from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import password_reset
from allauth.account.utils import user_pk_to_url_str


User = get_user_model()

# Create your models here.
@receiver(post_save, sender=User)
def set_user_permissions(sender, instance, created, **kwargs):
    if created and instance.role in (3,4):
        # add group nurse to user
        nurse_group = Group.objects.get(name='Nurse')
        nurse_group.user_set.add(instance)
        nurse_group.save()
        # # add all permissions in nurse group to user
        # nurse_permissions = Permission.objects.filter(group=nurse_group)
        # for permission in nurse_permissions:
        #     instance.user_permissions.add(permission)
        # instance.save()
    elif created and instance.role == 1:
        # add group district admin to user
        dist_admin_group = Group.objects.get(name='DistAdmin')
        dist_admin_group.user_set.add(instance)
        dist_admin_group.save()
        # # add all permissions in district admin group to user
        # dist_admin_permissions = Permission.objects.filter(group=dist_admin_group)
        # for permission in dist_admin_permissions:
        #     instance.user_permissions.add(permission)
        # instance.save()



@receiver(password_reset, sender=User)
def set_user_is_verified(sender, request,**kwargs):
    user = sender
    user.is_verified = True
    user.save()
