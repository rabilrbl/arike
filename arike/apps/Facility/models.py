from django.db import models
from arike.apps.System.models import BaseModel

# CHOICES
FACILITY_CHOICE = (
    (1, "PHC"),
    (2, "CHC"),
)


# Create your models here.
class Facility(BaseModel):
    ward = models.ForeignKey('arike.apps.System.models.Ward', on_delete=models.CASCADE)

    kind = models.IntegerField(choices=FACILITY_CHOICE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6)
    phone = models.CharField(max_length=10)