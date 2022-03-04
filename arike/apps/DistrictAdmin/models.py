from allauth.account.signals import password_reset
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from arike.apps.DistrictAdmin.signals import set_user_is_verified, set_user_permissions

User = get_user_model()

post_save.connect(set_user_permissions, sender=User)

password_reset.connect(set_user_is_verified, sender=User)
