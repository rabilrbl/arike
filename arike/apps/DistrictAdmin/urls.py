from django.urls import path


from arike.apps.DistrictAdmin.views import (
    UserIndexView,
    NewUser,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
)

app_name = "apps.DistrictAdmin"

urlpatterns = [
    path('', UserIndexView.as_view(), name='users'),
    path('add/', NewUser.as_view(), name='add'),
    path('view/<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='delete'),
]