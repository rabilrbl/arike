from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm
from django.shortcuts import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from arike.apps.Patient.models import Disease, Patient, PatientDisease


class DiseaseListView(PermissionRequiredMixin, ListView):
    model = PatientDisease
    template_name = 'Patient/disease/index.html'
    context_object_name = 'diseases'

    permission_required = 'Patient.view_patientdisease'

    def get_queryset(self):
        return PatientDisease.objects.filter(patient=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Disease History'
        context['patient'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context


class DiseaseCreateForm(ModelForm):
    class Meta:
        model = Disease
        fields = ['name', 'icds_code']


class DiseaseCreate(PermissionRequiredMixin, CreateView):
    model = Disease
    form_class = DiseaseCreateForm
    template_name = 'Patient/disease/create.html'

    permission_required = 'Patient.create_disease'

    def get_success_url(self) -> str:
        return f"/patient/{self.kwargs['pk']}/disease/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Disease'
        context['patient'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        if form.is_valid():
            p = PatientDisease.objects.filter(disease=form.instance).first()
            if not p:
                p = PatientDisease.objects.create(
                    patient=Patient.objects.get(pk=self.kwargs['pk']),
                    disease=Disease.objects.create(
                        name=form.instance.name,
                        icds_code=form.instance.icds_code
                    ),
                    user=self.request.user,
                    note=form.data['note']
                )
        return HttpResponseRedirect(self.get_success_url())

    def form_success(self, form):
        PatientDisease.objects.create(patient=Patient.objects.get(
            pk=self.kwargs['pk']), disease=form.instance, user=self.request.user, note=form.data['note'])
        return super().form_success(form)


class DiseaseUpdateView(PermissionRequiredMixin, UpdateView):
    model = Disease
    form_class = DiseaseCreateForm
    template_name = 'Patient/disease/update.html'

    permission_required = 'Patient.change_disease'

    def get_success_url(self) -> str:
        return f"/patient/{self.kwargs['pk']}/disease/"

    def get_object(self, queryset=None):
        return Disease.objects.get(pk=PatientDisease.objects.get(pk=self.kwargs['disease_id']).disease.pk)

    def form_valid(self, form):
        if form.is_valid():
            p = PatientDisease.objects.get(pk=self.kwargs['disease_id'])
            p.note = form.data['note']
            p.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Disease'
        context['patient'] = Patient.objects.get(pk=self.kwargs['pk'])
        context['note'] = PatientDisease.objects.get(pk=self.kwargs['disease_id']).note
        return context


class DiseaseDeleteView(PermissionRequiredMixin, DeleteView):
    model = Disease
    template_name = 'Patient/disease/delete.html'

    permission_required = 'Patient.delete_disease'

    def get_success_url(self) -> str:
        return f"/patient/{self.kwargs['pk']}/disease/"

    def get_object(self):
        return Disease.objects.get(pk=PatientDisease.objects.get(pk=self.kwargs['disease_id']).disease.pk)

    def form_valid(self, form):
        PatientDisease.objects.get(pk=self.kwargs['disease_id']).delete()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Disease'
        return context
