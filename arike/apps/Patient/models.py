from wsgiref.simple_server import demo_app
from django.db import models
from arike.users import choice_data as choices
from arike.apps.System.models import BaseModel, Ward
from arike.apps.Facility.models import Facility

# Create your models here.

class Patient(BaseModel):
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT,  default="")

    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(choices=choices.GENDER, default=choices.GENDER[2][0])
    phone = models.CharField(max_length=11, blank=True, null=True)
    emergency_phone_number = models.CharField(max_length=11)
    expired_time = models.DateTimeField(blank=True, null=True)