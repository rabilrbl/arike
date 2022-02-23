# Models
from arike.apps.Facility.models import Facility

# import GenericViews
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django.urls import reverse_lazy
User = 


class UserIndexView(ListView):
    """
    District Admin User list page
    """
    template_name = 'DistrictAdmin/index.html'
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Users'
        return context