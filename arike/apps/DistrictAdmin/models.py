from allauth.account.models import EmailAddress
from allauth.account.signals import password_reset
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

# Create your models here.


@receiver(post_save, sender=User)
def set_user_permissions(sender, instance, created, **kwargs):
    if created and instance.role in (3, 4):
        with transaction.atomic():
            # add group nurse to user
            nurse_group = Group.objects.get(name='Nurse')
            nurse_group.user_set.add(instance)
            nurse_group.save()
        # instance.save()
    elif created and instance.role == 1:
        with transaction.atomic():
            # add group district admin to user
            dist_admin_group = Group.objects.get(name='DistAdmin')
            dist_admin_group.user_set.add(instance)
            dist_admin_group.save()


@receiver(password_reset, sender=User)
def set_user_is_verified(request, user, **kwargs):
    with transaction.atomic():
        email_address = EmailAddress.objects.get(user=user)
        user.is_verified = email_address.verified = email_address.primary = True
        user.save()
        email_address.save()
