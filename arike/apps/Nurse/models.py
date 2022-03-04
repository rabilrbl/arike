from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from arike.apps.System.models import BaseModel

User = get_user_model()

# Create your models here.


class Reports(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    last_sent = models.DateTimeField(
        blank=True,
        null=True,
        default=datetime(
            datetime.today().year, datetime.today().month, datetime.today().day
        ),
        help_text="Choose time",
    )
    consent = models.BooleanField(
        default=False, help_text="Check this box if you want to receive the report"
    )

    def __str__(self):
        return (
            self.user.username
            + " Last Sent: "
            + self.last_sent.strftime("%d-%m-%Y %H:%M")
        )
