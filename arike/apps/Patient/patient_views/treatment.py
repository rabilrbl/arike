from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from arike.apps.Patient.models import Patient, Treatment


class TreatmentListView(PermissionRequiredMixin, ListView):
    model = Treatment
    template_name = 'Patient/treatment/index.html'
    context_object_name = 'treatments'

    permission_required = 'Patient.view_treatment'

    def get_queryset(self):
        return Treatment.objects.filter(patient=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Treatment List'
        context['patient'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context


class TreatmentCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TreatmentCreateForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'rows': '3'})

    class Meta:
        model = Treatment
        fields = ['care_type', 'care_sub_type', 'description']


class TreatmentCreate(PermissionRequiredMixin, CreateView):
    model = Treatment
    form_class = TreatmentCreateForm
    template_name = 'Patient/treatment/create.html'

    permission_required = 'Patient.add_treatment'

    def get_success_url(self) -> str:
        return f"/patient/{self.kwargs['pk']}/treatment/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Treatment'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.patient = Patient.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class TreatmentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Treatment
    form_class = TreatmentCreateForm
    template_name = 'Patient/treatment/update.html'

    pk_url_kwarg = 'treatment_id'

    permission_required = 'Patient.change_treatment'

    def get_success_url(self) -> str:
        return f"/patient/{self.kwargs['pk']}/treatment/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Treatment'
        return context


class TreatmentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Treatment
    template_name = 'Patient/treatment/delete.html'

    pk_url_kwarg = 'treatment_id'

    permission_required = 'Patient.delete_treatment'

    def get_success_url(self) -> str:
        return f"/patient/{self.kwargs['pk']}/treatment/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Treatment'
        return context
