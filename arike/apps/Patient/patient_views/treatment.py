from arike.apps.Patient.models import Patient, Treatment

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django import forms


class TreatmentListView(ListView):
    model = Treatment
    template_name = 'Patient/treatment/index.html'
    context_object_name = 'treatments'

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


class TreatmentCreate(CreateView):
    model = Treatment
    form_class = TreatmentCreateForm
    template_name = 'Patient/treatment/create.html'

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


class TreatmentUpdateView(UpdateView):
    model = Treatment
    form_class = TreatmentCreateForm
    template_name = 'Patient/treatment/update.html'

    pk_url_kwarg = 'treatment_id'

    def get_success_url(self) -> str:
        return f"/patient/{self.kwargs['pk']}/treatment/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Treatment'
        return context


class TreatmentDeleteView(DeleteView):
    model = Treatment
    template_name = 'Patient/treatment/delete.html'

    pk_url_kwarg = 'treatment_id'

    def get_success_url(self) -> str:
        return f"/patient/{self.kwargs['pk']}/treatment/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Treatment'
        return context