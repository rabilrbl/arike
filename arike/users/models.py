from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from arike.users import choice_data as choices
from arike.apps.System.models import District
from arike.apps.Facility.models import Facility


class User(AbstractUser):
    """
    Default custom user model for arike.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    district = models.ForeignKey(District, on_delete=models.PROTECT, default="")
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, default="")

    #: First and last name do not cover name patterns around the globe
    full_name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    role = models.CharField(max_length=3, choices=choices.UserRoles, default=choices.UserRoles[1][0])
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=11, blank=True)
    gender = models.IntegerField(choices=choices.GENDER, default=choices.GENDER[2][0])

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
