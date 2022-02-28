from pydoc import cram
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from arike.apps.Patient.models import VisitSchedule, Treatment, Patient
from django.forms import ModelForm
from arike.apps.Nurse.filters import TreatmentFilter
# from arike.users.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class ScheduleList(PermissionRequiredMixin, ListView):
    template_name = 'Nurse/schedule.html'
    context_object_name = 'schedules'

    permission_required = 'Patient.view_visitschedule'

    def filter_queryset(self, queryset):
        self.myfilter = TreatmentFilter(self.request.GET, queryset=queryset)
        return self.myfilter.qs

    def get_queryset(self):
        queryset = VisitSchedule.objects.filter(user=self.request.user)
        return self.filter_queryset(queryset)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Schedule'
        context['myfilter'] = self.myfilter
        return context


class ScheduleVisitForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = VisitSchedule
        fields = ['patient', 'date', 'time', 'duration']


class ScheduleVisit(PermissionRequiredMixin,CreateView):
    template_name = 'Nurse/schedule_visit.html'
    form_class = ScheduleVisitForm
    context_object_name = 'schedule'
    success_url = '/schedule/'

    permission_required = 'Patient.create_visitschedule'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Schedule Visit'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class AgendaView(PermissionRequiredMixin,ListView):
    template_name = 'Nurse/agenda.html'
    context_object_name = 'agenda'

    permission_required = 'Patient.view_visitschedule'

    def get_queryset(self):
        queryset = VisitSchedule.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agenda'
        return context