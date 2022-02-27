from django.urls import path

from arike.apps.Patient.views import (
    PatientIndexView,
    PatientDetailView,
    CreatePatient,
    UpdatePatient,
    DeletePatient,
)

from arike.apps.Patient.patient_views.visits import (
    VisitHistory,
    VisitDetailView,
)

from arike.apps.Patient.patient_views.family import (
    FamilyListView,
    FamilyDetailCreate,
    FamilyDetailUpdateView,
    FamilyDetailDeleteView
)

from arike.apps.Patient.patient_views.disease import (
    DiseaseListView,
    DiseaseCreate,
    DiseaseUpdateView,
    DiseaseDeleteView
)

from arike.apps.Patient.patient_views.treatment import (
    TreatmentListView,
    TreatmentCreate,
    TreatmentUpdateView,
    TreatmentDeleteView
)

app_name = "Patient"

urlpatterns = [
    path('', PatientIndexView.as_view(), name='patients'),
    path('create/', CreatePatient.as_view(), name='add'),
    path('<int:pk>/', PatientDetailView.as_view(), name='view'),
    path('update/<int:pk>/', UpdatePatient.as_view(), name='update'),
    path('delete/<int:pk>/', DeletePatient.as_view(), name='delete'),

    path('<int:pk>/visits/', VisitHistory.as_view(), name='visits'),
    path('<int:pk>/visits/<int:visit_id>/', VisitDetailView.as_view(), name='visit_history'),

    path('<int:pk>/family/', FamilyListView.as_view(), name='family'),
    path('<int:pk>/family/create/', FamilyDetailCreate.as_view(), name='family_create'),
    path('<int:pk>/family/update/<int:family_id>/', FamilyDetailUpdateView.as_view(), name='family_update'),
    path('<int:pk>/family/delete/<int:family_id>/', FamilyDetailDeleteView.as_view(), name='family_delete'),

    path('<int:pk>/disease/', DiseaseListView.as_view(), name='disease'),
    path('<int:pk>/disease/create/', DiseaseCreate.as_view(), name='disease_create'),
    path('<int:pk>/disease/update/<int:disease_id>/', DiseaseUpdateView.as_view(), name='disease_update'),
    path('<int:pk>/disease/delete/<int:disease_id>/', DiseaseDeleteView.as_view(), name='disease_delete'),

    path('<int:pk>/treatment/', TreatmentListView.as_view(), name='treatment'),
    path('<int:pk>/treatment/create/', TreatmentCreate.as_view(), name='treatment_create'),
    path('<int:pk>/treatment/update/<int:treatment_id>/', TreatmentUpdateView.as_view(), name='treatment_update'),
    path('<int:pk>/treatment/delete/<int:treatment_id>/', TreatmentDeleteView.as_view(), name='treatment_delete'),

]