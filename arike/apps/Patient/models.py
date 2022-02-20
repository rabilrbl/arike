from django.db import models
from arike.users import choice_data
from arike.apps.System.models import BaseModel

# Create your models here.

class Patient(BaseModel):
    ward = models.ForeignKey('ward.Ward', on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    gender = models.IntegerField(choices=choice_data.GENDER)
    phone = models.CharField(max_length=10)
    emergency_phone_number = models.CharField(max_length=10)
    expired_time = models.DateTimeField(blank=True, null=True)