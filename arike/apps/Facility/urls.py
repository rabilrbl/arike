from django.urls import path

from arike.apps.Facility.views import (
    CreateFacility,
    DeleteFacility,
    DetailViewFacility,
    IndexViewFacilities,
    UpdateFacility,
)

app_name = "apps.Facility"

# URLS
urlpatterns = [
    path("", IndexViewFacilities.as_view(), name="index"),
    path("add/", CreateFacility.as_view(), name="add"),
    path("update/<pk>/", UpdateFacility.as_view(), name="update"),
    path("view/<pk>/", DetailViewFacility.as_view(), name="view"),
    path("delete/<pk>/", DeleteFacility.as_view(), name="delete"),
]
