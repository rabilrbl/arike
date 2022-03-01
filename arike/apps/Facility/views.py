from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from arike.apps.Facility.filters import FacilityFilter
from arike.apps.Facility.models import Facility

# Create your views here.


class IndexViewFacilities(PermissionRequiredMixin, ListView):
    """
    Index page for Facility
    """
    template_name = 'Facility/facilities.html'
    context_object_name = "facilities"

    permission_required = 'Facility.view_facility'

    def filter_queryset(self, queryset):
        self.myFilter = FacilityFilter(self.request.GET, queryset=queryset)
        return self.myFilter.qs

    def get_queryset(self):
        queryset = Facility.objects.all()
        queryset = self.filter_queryset(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Facilities'
        context['sfield'] = "name"
        context['myfilter'] = self.myFilter
        return context


class DetailViewFacility(PermissionRequiredMixin, DetailView):
    """
    Detail page for each Facility
    """
    template_name = 'Facility/detail_facility.html'
    model = Facility
    context_object_name = "facility"

    permission_required = 'Facility.view_facility'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Facility'
        return context


class CreateFacilityForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'px-4 py-3 rounded-xl border border-gray-400 focus:outline-none focus:border-gray-500 text-xl'})
        self.fields['address'].widget.attrs.update(
            {'class': 'px-4 py-3 rounded-xl border border-gray-400 focus:outline-none focus:border-gray-500 text-xl', 'rows': '2'})
        self.fields['ward'].widget.attrs.update(
            {'class': 'px-4 py-3 rounded-xl border border-gray-400 focus:outline-none focus:border-gray-500 text-xl'})
        self.fields['pincode'].widget.attrs.update(
            {'class': 'px-4 py-3 rounded-xl border border-gray-400 focus:outline-none focus:border-gray-500 text-xl'})
        self.fields['phone'].widget.attrs.update(
            {'class': 'px-4 py-3 rounded-xl border border-gray-400 focus:outline-none focus:border-gray-500 text-xl'})

    class Meta:
        model = Facility
        fields = ['kind', 'name', 'address', 'ward', 'pincode', 'phone']


class CreateFacility(PermissionRequiredMixin, CreateView):
    """
    Create page for new Facility  
    """
    form_class = CreateFacilityForm
    template_name = 'Facility/create_facility.html'
    success_url = reverse_lazy('facility:index')

    permission_required = 'Facility.add_facility'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Facility'
        return context


class UpdateFacility(PermissionRequiredMixin, UpdateView):
    """
    Update page for existing Facility
    """
    model = Facility
    form_class = CreateFacilityForm
    template_name = 'Facility/update_facility.html'
    success_url = reverse_lazy('facility:index')

    permission_required = 'Facility.change_facility'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Facility'
        return context


class DeleteFacility(PermissionRequiredMixin, DeleteView):
    """
    Delete page for existing Facility
    """
    template_name = 'Facility/delete_facility.html'
    model = Facility
    success_url = reverse_lazy('facility:index')

    permission_required = 'Facility.delete_facility'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Facility'
        return context
