from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from arike.apps.Facility.models import Facility
from arike.apps.Patient.tasks import send_report_to_family_members
from arike.apps.System.models import BaseModel, Ward
from arike.users import choice_data as choices

User = get_user_model()

# Create your models here.


class Patient(BaseModel):
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, default="")

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
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )


RELATION = (
    (1, "Father"),
    (2, "Mother"),
    (3, "Brother"),
    (4, "Sister"),
    (5, "Spouse"),
    (6, "Child"),
    (7, "Grandfather"),
    (8, "Grandmother"),
    (9, "Other"),
)

EDUCATION = (
    (1, "School"),
    (2, "College"),
    (3, "Graduate"),
    (4, "Post Graduate"),
    (5, "Doctorate"),
    (6, "Other"),
)

ICDS_CODE = (
    ("D-32", "DM"),
    ("HT-58", "Hypertension"),
    ("IDH-21", "IHD"),
    ("DPOC-144", "COPD"),
    ("DM-62", "Dementia"),
    ("CAV-89", "CVA"),
    ("C-98", "Cancer"),
    ("DC-25", "CKD"),
)


class FamilyDetail(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    date_of_birth = models.DateField()
    email = models.EmailField(blank=True, null=True)
    relation = models.IntegerField(choices=RELATION, default=RELATION[8][0])
    address = models.TextField()
    education = models.IntegerField(choices=EDUCATION, default=EDUCATION[5][0])
    occupation = models.CharField(max_length=255, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Disease(BaseModel):
    name = models.CharField(max_length=255)
    icds_code = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class PatientDisease(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    disease = models.ForeignKey(Disease, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
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
        return self.date.strftime("%d-%m-%Y") + " @ " + self.time.strftime("%I:%M %p")


PALLIATIVE_PHASE = (
    (1, "Stable"),
    (2, "Unstable"),
    (3, "Deteriorating"),
    (4, "Dying"),
)

SYSTEMIC_EXAMINATION = (
    (1, "Cardiovascular"),
    (2, "Gastrointestinal"),
    (3, "Central nervous system"),
    (4, "Respiratory"),
    (5, "Genital-urinary"),
)


class VisitDetail(BaseModel):
    visit_schedule = models.ForeignKey(VisitSchedule, on_delete=models.PROTECT)

    palliative_phase = models.IntegerField(
        choices=PALLIATIVE_PHASE, default=PALLIATIVE_PHASE[0][0]
    )
    blood_pressure = models.IntegerField(blank=True, null=True)
    pulse = models.IntegerField(blank=True, null=True)
    general_random_blood_pressure = models.IntegerField(blank=True, null=True)
    personal_hygiene = models.TextField(blank=True, null=True)
    mouth_hygiene = models.TextField(blank=True, null=True)
    public_hygiene = models.TextField(blank=True, null=True)
    systemic_examination = models.IntegerField(
        choices=SYSTEMIC_EXAMINATION, default=SYSTEMIC_EXAMINATION[0][0]
    )
    patient_at_peace = models.BooleanField(
        default=False, choices=((True, "Yes"), (False, "No"))
    )
    pain = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return (
            self.visit_schedule.patient.full_name
            + " - "
            + self.visit_schedule.date.strftime("%d-%m-%Y")
            + " - "
            + self.visit_schedule.time.strftime("%H:%M")
        )  # noqa: E501


# Ref for treatments https://github.com/coronasafe/arike/blob/main/db/seeds/development/treatment.seeds.rb


class Treatment(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True, default=None
    )

    description = models.TextField()
    care_type = models.CharField(max_length=255, blank=True, null=True)
    care_sub_type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.care_type + " - " + self.care_sub_type


class TreatmentNotes(BaseModel):
    treatment = models.ForeignKey(Treatment, on_delete=models.PROTECT)
    visit = models.ForeignKey(VisitDetail, on_delete=models.PROTECT)

    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.treatment.patient.full_name + " - " + self.treatment.care_type


@receiver(post_save, sender=VisitDetail)
def send_report_to_family_members_on_save(sender, instance, **kwargs):
    print(
        f"Sending report to family members of {instance.visit_schedule.patient.full_name}.."
    )
    # Hardcoding data & famdata because I got error when I tried to to use model.values()
    # TODO : Fix this
    # Data to be sent to family members
    data = {
        "full_name": instance.visit_schedule.patient.full_name,
        "palliative_phase": instance.get_palliative_phase_display(),
        "blood_pressure": instance.blood_pressure,
        "pulse": instance.pulse,
        "general_random_blood_pressure": instance.general_random_blood_pressure,
        "personal_hygiene": instance.personal_hygiene,
        "mouth_hygiene": instance.mouth_hygiene,
        "public_hygiene": instance.public_hygiene,
        "systemic_examination": instance.get_systemic_examination_display(),
        "patient_at_peace": instance.get_patient_at_peace_display(),
        "note": instance.note,
    }
    famdata = FamilyDetail.objects.filter(patient=instance.visit_schedule.patient)
    family = []
    for fam in famdata:
        temp = {
            "full_name": fam.full_name,
            "email": fam.email,
        }
        family.append(temp)

    send_report_to_family_members.delay(data, family)
