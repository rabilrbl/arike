from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from arike.users import choice_data as choices


class User(AbstractUser):
    """
    Default custom user model for arike.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    full_name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    role = models.CharField(max_length=3, choice=choices.UserRoles)
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, blank=True)
    gender = models.IntegerField(choices=choices.GENDER)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
