import random
import string

from urllib import request
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from arike.users import choice_data as choices
from arike.apps.System.models import District, BaseModel
from arike.apps.Facility.models import Facility
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)



class User(AbstractUser, BaseModel):
    """
    Default custom user model for arike.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, default=None)
    facility = models.ForeignKey(Facility,verbose_name=_("Assign Facility"), on_delete=models.PROTECT, null=True, default=None)

    #: First and last name do not cover name patterns around the globe
    full_name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    role = models.IntegerField(choices=choices.UserRole, default=choices.UserRole[2][0], verbose_name=_("User Role"))
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=11, blank=True)
    gender = models.IntegerField(choices=choices.GENDER, default=choices.GENDER[2][0])

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.facility is None:
            self.district = self.facility.ward.local_body.district
        if not self.username:
            self.username = self.get_random_username()
        super().save(*args, **kwargs)
    
    def get_random_username(self):
        """Generate random username.

        Returns:
            str: Random username.

        """
        username = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=10)
        )
        while self.__class__.objects.filter(username=username).exists():
            username = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=10)
            )
        return username

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"external_id": self.external_id})

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"
