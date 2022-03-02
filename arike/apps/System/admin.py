from django.contrib import admin

from arike.apps.System.models import District, LocalBody, State

# Register your models here.
admin.site.register(District)
admin.site.register(LocalBody)
admin.site.register(State)
