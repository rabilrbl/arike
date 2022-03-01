from django.contrib import admin

from arike.apps.Patient.models import *

# Register your models here.
# Register all models from facility app
admin.site.register(Ward)
admin.site.register(Patient)
admin.site.register(FamilyDetail)
admin.site.register(Disease)
admin.site.register(PatientDisease)
admin.site.register(VisitDetail)
admin.site.register(VisitSchedule)
admin.site.register(Treatment)
admin.site.register(TreatmentNotes)
