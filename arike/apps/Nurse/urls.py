from django.urls import path
from arike.apps.Nurse.views import (
    ScheduleList,
    ScheduleVisit,
)

app_name = 'nurse'

urlpatterns = [
    path('', ScheduleList.as_view(), name='schedule'),
    path('visit/', ScheduleVisit.as_view(), name='schedule_visit'),
]