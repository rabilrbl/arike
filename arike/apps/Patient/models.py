from wsgiref.simple_server import demo_app
from django.db import models
from arike.users import choice_data as choices
from arike.apps.System.models import BaseModel, Ward
from arike.apps.Facility.models import Facility
from datetime import date, datetime
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Patient(BaseModel):
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT,  default="")

    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    address = models.TextField()
    landmark = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(choices=choices.GENDER, default=choices.GENDER[2][0])
    phone = models.CharField(max_length=11, blank=True, null=True)
    emergency_phone_number = models.CharField(max_length=11)
    expired_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.full_name
    
    def calculate_age(self) -> int:
        """
        Calculate age from date of birth
        """
        today = datetime.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


RELATION = (
    (1, 'Father'),
    (2, 'Mother'),
    (3, 'Brother'),
    (4, 'Sister'),
    (5, 'Spouse'),
    (6, 'Child'),
    (7, 'Grandfather'),
    (8, 'Grandmother'),
    (9, 'Other'),
)

ICDS_CODE = (
    ("D-32","DM"),
    ("HT-58","Hypertension"),
    ("IDH-21","IHD"),
    ("DPOC-144","COPD"),
    ("DM-62","Dementia"),
    ("CAV-89","CVA"),
    ("C-98","Cancer"),
    ("DC-25","CKD")
)

class FamilyDetail(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True, null=True)
    relation = models.IntegerField(choices=RELATION, default=RELATION[0][0])
    address = models.TextField()
    education = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Disease(BaseModel):
    name = models.CharField(max_length=255)
    icd_code = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PatientDisease(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    disease = models.ForeignKey(Disease, on_delete=models.PROTECT)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.patient.full_name + " - " + self.disease.name


class VisitSchedule(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(default=30)

    def __str__(self):
        return self.patient.full_name + " - " + self.date.strftime("%d-%m-%Y") + " - " + self.time.strftime("%H:%M")


class Symptoms(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class VisitDetail(BaseModel):
    visit_schedule = models.ForeignKey(VisitSchedule, on_delete=models.PROTECT)

    palliative_phase = models.CharField(max_length=255, blank=True, null=True)
    blood_pressure = models.IntegerField(blank=True, null=True)
    pulse = models.IntegerField(blank=True, null=True)
    general_random_blood_pressure = models.IntegerField(blank=True, null=True)
    personal_hygiene = models.CharField(max_length=255, blank=True, null=True)
    mouth_hygiene = models.CharField(max_length=255, blank=True, null=True)
    public_hygiene = models.CharField(max_length=255, blank=True, null=True)
    systemic_examination = models.CharField(max_length=255, blank=True, null=True)
    patient_at_peace = models.BooleanField(default=False)
    pain = models.BooleanField(default=False)
    symptoms = models.ManyToManyField(Symptoms, blank=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.visit_schedule.patient.full_name + " - " + self.visit_schedule.date.strftime("%d-%m-%Y") + " - " + self.visit_schedule.time.strftime("%H:%M")


# Ref for treatments https://github.com/coronasafe/arike/blob/main/db/seeds/development/treatment.seeds.rb

class Treatment(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    description = models.CharField(max_length=255)
    care_type = models.CharField(max_length=255)
    care_sub_type = models.CharField(max_length=255)

    def __str__(self):
        return self.patient.full_name + " - " + self.care_type


class TreatmentNotes(BaseModel):
    treatment = models.ForeignKey(Treatment, on_delete=models.PROTECT)
    visit = models.ForeignKey(VisitDetail, on_delete=models.PROTECT)

    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.treatment.patient.full_name + " - " + self.treatment.care_type
