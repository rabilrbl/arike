from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from arike.apps.Patient.filters import PatientFilter
from arike.apps.Patient.models import Patient, VisitSchedule
from arike.users import choice_data as choices


class PatientIndexView(PermissionRequiredMixin, ListView):
    """
    Patient list page
    """
    template_name = 'Patient/patients.html'
    context_object_name = "patients"

    permission_required = 'Patient.view_patient'

    def filter_queryset(self, queryset):
        self.myFilter = PatientFilter(self.request.GET, queryset=queryset)
        return self.myFilter.qs

    def get_queryset(self):
        queryset = Patient.objects.filter(facility=self.request.user.facility)
        queryset = self.filter_queryset(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Patients'
        context['sfield'] = "full_name"
        context['myfilter'] = self.myFilter
        return context


class PatientDetailView(PermissionRequiredMixin, DetailView):
    """
    Patient detail page
    """

    model = Patient
    template_name = 'Patient/detail_patient.html'

    permission_required = 'Patient.view_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Patient'
        context['last_visit'] = VisitSchedule.objects.filter(patient=self.object).order_by('-date').first()
        # TODO: add next visit date
        # context['next_visit'] =
        return context


class PatientForm(ModelForm):
    """
    Pateint form
    """

    def __init__(self, *args, **kwargs):
        className = "px-4 py-2 rounded-xl border border-gray-400 focus:outline-none focus:border-gray-500"
        super().__init__(*args, **kwargs)
        self.fields['gender'] = forms.ChoiceField(widget=widgets.AdminRadioSelect, choices=choices.GENDER)
        self.fields['date_of_birth'] = forms.DateField(widget=widgets.AdminDateWidget)
        self.fields['full_name'].widget.attrs.update({
            "class": className,
        })
        self.fields['date_of_birth'].widget.attrs.update({
            "class": className,
        })
        self.fields['address'].widget.attrs.update({
            "class": className,
            "rows": "3",
        })
        self.fields['landmark'].widget.attrs.update({
            "class": className,
        })
        self.fields['ward'].widget.attrs.update({
            "class": className,
        })
        self.fields['facility'].widget.attrs.update({
            "class": className,
        })
        self.fields['gender'].widget.attrs.update({
            "class": className,
        })

    class Meta:
        model = Patient
        fields = ['full_name', 'date_of_birth', 'address', 'landmark',
                  'ward', 'facility', 'phone', 'emergency_phone_number', 'gender']


class CreatePatient(PermissionRequiredMixin, CreateView):
    form_class = PatientForm
    template_name = 'Patient/create_patient.html'
    success_url = reverse_lazy('patient:patients')

    permission_required = 'Patient.add_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Patient'
        return context


class UpdatePatient(PermissionRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'Patient/update_patient.html'
    success_url = reverse_lazy('patient:patients')

    permission_required = 'Patient.change_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Patient'
        return context


class DeletePatient(PermissionRequiredMixin, DeleteView):
    model = Patient
    template_name = 'Patient/delete_patient.html'
    success_url = reverse_lazy('patient:patients')

    permission_required = 'Patient.delete_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Patient'
        return context
