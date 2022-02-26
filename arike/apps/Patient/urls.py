from django.urls import path

from arike.apps.Patient.views import (
    PatientIndexView,
    PatientDetailView,
    CreatePatient,
    UpdatePatient,
    DeletePatient,
)

app_name = "Patient"

urlpatterns = [
    path('', PatientIndexView.as_view(), name='patients'),
    path('create/', CreatePatient.as_view(), name='add'),
    path('<int:pk>/', PatientDetailView.as_view(), name='view'),
    path('update/<int:pk>/', UpdatePatient.as_view(), name='update'),
    path('delete/<int:pk>/', DeletePatient.as_view(), name='delete'),
]