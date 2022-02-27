from django.contrib import admin
# import all models from facility app
from arike.apps.Facility.models import *

# Register your models here.
admin.site.register(Facility)

