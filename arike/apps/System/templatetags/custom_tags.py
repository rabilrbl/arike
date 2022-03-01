from django.template import Library
from arike.apps.Patient.models import Treatment
from arike.apps.System.models import Ward
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()

register = Library()


@register.simple_tag(takes_context=True)
def treatment(context, patient):
    context['treatments'] = Treatment.objects.filter(patient=patient)
    return ''


@register.simple_tag
def filter_day(queryset, day):
    if day == "today":
        return queryset.filter(date=datetime.today())
    elif day == "tomorrow":
        return queryset.filter(date=datetime.today() + timedelta(days=1))
    elif day == "all":
        return queryset.filter(date__gt=datetime.today() + timedelta(days=1))
    else:
        raise ValueError("Invalid day, choose from [today, tomorrow, all]")
