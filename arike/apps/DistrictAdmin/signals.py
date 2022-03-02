from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group
from django.db import transaction


def set_user_permissions(sender, instance, created, **kwargs):
    if created and instance.role in (3, 4):
        with transaction.atomic():
            # add group nurse to user
            nurse_group = Group.objects.get(name='Nurse')
            nurse_group.user_set.add(instance)
            nurse_group.save()
    elif created and instance.role == 1:
        with transaction.atomic():
            # add group district admin to user
            dist_admin_group = Group.objects.get(name='DistAdmin')
            dist_admin_group.user_set.add(instance)
            dist_admin_group.save()


def set_user_is_verified(request, user, **kwargs):
    with transaction.atomic():
        email_address = EmailAddress.objects.get(user=user)
        user.is_verified = email_address.verified = email_address.primary = True
        user.save()
        email_address.save()
