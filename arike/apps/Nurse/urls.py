from django.urls import path
from arike.apps.Nurse.views import (
    ScheduleList,
    ScheduleVisit,
    UnscheduleVisit,
    AgendaView,
    VisitAgendaView,
    HealthInfoView,
    TreatmentNoteView,
    ReportsConsentView,
)

app_name = 'nurse'

urlpatterns = [
    path('', ScheduleList.as_view(), name='schedule'),
    path('visit/', ScheduleVisit.as_view(), name='schedule_visit'),
    path('unschedule/<int:pk>/', UnscheduleVisit.as_view(), name='unschedule_visit'),
    path('agenda/', AgendaView.as_view(), name='agenda'),
    path('agenda/<int:patient_id>/visit/<int:pk>/', VisitAgendaView.as_view(), name='visit_agenda'),
    path('healthinfo/<int:pk>/', HealthInfoView.as_view(), name='healthinfo'),
    path('<int:patient_id>/treatmentnote/<int:pk>/', TreatmentNoteView.as_view(), name='treatmentnote'),
    path('reports/', ReportsConsentView.as_view(), name='reports_consent'),
]