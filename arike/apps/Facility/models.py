from django.db import models
from arike.apps.System.models import BaseModel, Ward

# CHOICES
FACILITY_CHOICE = (
    (1, "PHC"),
    (2, "CHC"),
)


# Create your models here.
class Facility(BaseModel):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=True)

    kind = models.IntegerField(choices=FACILITY_CHOICE)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=6)
    phone = models.CharField(max_length=11)


    def __str__(self):
        return f"{self.name} ({self.get_kind_display()})"