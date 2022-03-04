from datetime import datetime

from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ModelForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from arike.apps.Nurse.filters import TreatmentFilter
from arike.apps.Nurse.models import Reports
from arike.apps.Patient.models import (
    Patient,
    Treatment,
    TreatmentNotes,
    VisitDetail,
    VisitSchedule,
)


class ScheduleList(PermissionRequiredMixin, ListView):
    template_name = "Nurse/schedule.html"
    context_object_name = "patients"

    permission_required = "Patient.view_patient"

    def filter_queryset(self, queryset):
        self.myfilter = TreatmentFilter(self.request.GET, queryset=queryset)
        return self.myfilter.qs

    def get_queryset(self):
        queryset = Patient.objects.all()
        return self.filter_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Schedule"
        context["myfilter"] = self.myfilter
        return context


class ScheduleVisitForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = VisitSchedule
        fields = ["patient", "date", "time", "duration"]


class ScheduleVisit(PermissionRequiredMixin, CreateView):
    template_name = "Nurse/schedule_visit.html"
    form_class = ScheduleVisitForm
    context_object_name = "schedule"
    success_url = "/schedule/"

    permission_required = "Patient.add_visitschedule"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Schedule Visit"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UnscheduleVisit(PermissionRequiredMixin, DeleteView):
    model = VisitSchedule
    template_name = "Nurse/unschedule_visit.html"
    context_object_name = "schedule"

    permission_required = "Patient.delete_visitschedule"

    def get_success_url(self):
        return self.request.GET.get("next", "/schedule/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Unschedule Visit"
        return context


class AgendaView(PermissionRequiredMixin, ListView):
    model = VisitSchedule
    template_name = "Nurse/agenda.html"
    context_object_name = "agenda"

    permission_required = "Patient.view_visitschedule"

    def get_queryset(self):
        queryset = (
            VisitSchedule.objects.filter(
                user=self.request.user, date__gte=datetime.today().date()
            )
            .order_by("date", "time")
            .exclude(
                id__in=VisitDetail.objects.filter(
                    visit_schedule__user=self.request.user,
                    visit_schedule__date__gte=datetime.today().date(),
                ).values("visit_schedule")
            )
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Agenda"
        return context


class VisitAgendaView(PermissionRequiredMixin, View):
    permission_required = "Patient.view_visitschedule"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "Nurse/agenda_visit.html",
            {"pk": kwargs["pk"], "patient_id": kwargs["patient_id"]},
        )


class HealthInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["patient_at_peace"] = forms.ChoiceField(
            widget=widgets.AdminRadioSelect, choices=((True, "Yes"), (False, "No"))
        )
        self.fields["patient_at_peace"].label = "Is the patient at peace?"
        self.fields["note"].widget.attrs["rows"] = 3
        self.fields["public_hygiene"].widget.attrs["rows"] = 3
        self.fields["personal_hygiene"].widget.attrs["rows"] = 3
        self.fields["mouth_hygiene"].widget.attrs["rows"] = 3

    class Meta:
        model = VisitDetail
        fields = [
            "palliative_phase",
            "blood_pressure",
            "pulse",
            "general_random_blood_pressure",
            "patient_at_peace",
            "public_hygiene",
            "personal_hygiene",
            "mouth_hygiene",
            "systemic_examination",
            "note",
        ]


class HealthInfoView(PermissionRequiredMixin, CreateView):
    form_class = HealthInfoForm
    template_name = "Nurse/health_info.html"
    context_object_name = "health_info"

    permission_required = "Patient.add_visitdetail"

    def get_success_url(self):
        return reverse_lazy("nurse:agenda")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Health Info"
        return context

    def form_valid(self, form):
        form.instance.visit_schedule = VisitSchedule.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)


class TreatmentNoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["note"].widget.attrs["rows"] = 3

    class Meta:
        model = TreatmentNotes
        fields = ["note", "treatment"]


class TreatmentNoteView(PermissionRequiredMixin, CreateView):
    form_class = TreatmentNoteForm
    template_name = "Nurse/treatment_note.html"
    context_object_name = "treatment_note"

    permission_required = "Patient.add_treatmentnotes"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["treatment"].queryset = Treatment.objects.filter(
            patient=self.kwargs["patient_id"]
        )
        return form

    def get_success_url(self):
        return reverse_lazy("nurse:agenda")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Treatment Note"
        return context

    def form_valid(self, form):
        form.instance.visit_schedule = VisitSchedule.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)


class ReportsConsentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["last_sent"].widget.attrs.update({"class": "rounded-xl"})

    class Meta:
        model = Reports
        fields = ["last_sent", "consent"]


class ReportsConsentView(PermissionRequiredMixin, UpdateView):
    form_class = ReportsConsentForm
    template_name = "Nurse/reports_consent.html"
    context_object_name = "reports_consent"
    success_url = "/"

    permission_required = "Patient.add_visitdetail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Reports Consent"
        return context

    def get_object(self, queryset=None):
        return Reports.objects.get_or_create(user=self.request.user)[0]

    def form_valid(self, form):
        time = self.request.POST["time"].split(":")
        form.instance.last_sent = form.instance.last_sent.replace(
            hour=int(time[0]), minute=int(time[1])
        )
        return super().form_valid(form)
