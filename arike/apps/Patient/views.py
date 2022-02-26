
# import GenericViews
from dataclasses import field
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django import forms
from django.urls import reverse_lazy
from arike.apps.Patient.models import Patient
from arike.users import choice_data as choices
from django.contrib.admin import widgets


class PatientIndexView(ListView):
    """
    Patient list page
    """
    template_name = 'Patient/patients.html'
    context_object_name = "patients"

    def get_queryset(self):
        return Patient.objects.filter(deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Patients'
        return context


class PatientDetailView(DetailView):
    """
    Patient detail page
    """
    model = Patient
    template_name = 'Patient/detail_patient.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Patient'
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
        fields = ['full_name','date_of_birth','address','landmark','ward', 'facility','phone','emergency_phone_number','gender']


class CreatePatient(CreateView):
    form_class = PatientForm
    template_name = 'Patient/create_patient.html'
    success_url = reverse_lazy('patient:patients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Patient'
        return context


class UpdatePatient(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'Patient/update_patient.html'
    success_url = reverse_lazy('patient:patients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Patient'
        return context


class DeletePatient(DeleteView):
    model = Patient
    template_name = 'Patient/delete_patient.html'
    success_url = reverse_lazy('patient:patients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Patient'
        return context
