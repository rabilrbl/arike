from django.contrib.admin import widgets
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from arike.apps.Patient.models import FamilyDetail, Patient


class FamilyListView(PermissionRequiredMixin, ListView):
    model = FamilyDetail
    template_name = 'Patient/family_details/index.html'
    context_object_name = 'family'

    permission_required = 'Patient.view_familydetail'

    def get_queryset(self):
        return FamilyDetail.objects.filter(patient=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Family Details'
        context['patient'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context


class FamilyDetailCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(FamilyDetailCreateForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'rows': 2})
        self.fields['date_of_birth'].widget = widgets.AdminDateWidget()
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form rounded-lg'})

    class Meta:
        model = FamilyDetail
        fields = ['full_name', 'email', 'date_of_birth', 'phone', 'relation', 'education', 'occupation', 'address']


class FamilyDetailCreate(PermissionRequiredMixin, CreateView):
    model = FamilyDetail
    form_class = FamilyDetailCreateForm
    template_name = 'Patient/family_details/create.html'

    permission_required = 'Patient.add_familydetail'

    def get_success_url(self):
        return reverse_lazy('patient:family', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Family Detail'
        context['patient'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.patient = Patient.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class FamilyDetailUpdateView(PermissionRequiredMixin, UpdateView):
    model = FamilyDetail
    form_class = FamilyDetailCreateForm
    template_name = 'Patient/family_details/update.html'

    pk_url_kwarg = 'family_id'

    permission_required = 'Patient.change_familydetail'

    def get_success_url(self):
        return reverse_lazy('patient:family', kwargs={'pk': self.kwargs['pk']})

    def get_queryset(self):
        return FamilyDetail.objects.filter(patient=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Family Detail'
        return context


class FamilyDetailDeleteView(PermissionRequiredMixin, DeleteView):
    model = FamilyDetail
    template_name = 'Patient/family_details/delete.html'

    pk_url_kwarg = 'family_id'

    context_object_name = 'family'

    permission_required = 'Patient.delete_familydetail'

    def get_success_url(self):
        return reverse_lazy('patient:family', kwargs={'pk': self.kwargs['pk']})

    def get_queryset(self):
        return FamilyDetail.objects.filter(patient=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Family Detail'
        context['patient'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context
