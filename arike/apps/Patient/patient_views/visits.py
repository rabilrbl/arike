from django.views.generic import ListView
from django.views.generic.detail import DetailView
from arike.apps.Patient.models import VisitDetail
from arike.apps.Patient.models import Patient


class VisitHistory(ListView):
    model = VisitDetail
    template_name = 'Patient/visits/history.html'
    context_object_name = 'visits'

    def get_queryset(self):
        return VisitDetail.objects.filter(visit_schedule__patient=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Visit History'
        context['patient'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context

    
class VisitDetailView(DetailView):
    model = VisitDetail
    template_name = 'Patient/visits/detail.html'
    context_object_name = 'visit'

    def get_queryset(self):
        return VisitDetail.objects.filter(visit_schedule__patient=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Visit Detail'
        return context